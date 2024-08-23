local M = {}
local NuiPopup  = require('nui.popup')
local user = nil
local make_buffer_read_only = require("pieces_utils").make_buffer_read_only
local function create_ui(content, default_hl)
  local status_popup = NuiPopup({
    relative = "editor",
    border = {
      highlight = "FloatBorder",
      style = "rounded",
      text = {
        top = " Pieces Auth Status ",
      },
    },
    position = "50%",
    size = {
      width = "60%",
      height = "50%",
    },
    win_options = {
      wrap = true,
      linebreak = true,
      foldcolumn = "1",
      winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
    }
  })

  status_popup:mount()
  make_buffer_read_only(status_popup.bufnr)

  local ns_id = vim.api.nvim_create_namespace('pieces_ui')
  local logout_line
  for i, line in ipairs(content) do
    local hl = line[2] or default_hl
    local text = line[1]
    vim.api.nvim_buf_set_lines(status_popup.bufnr, i - 1, i, false, { text })

    -- Highlight specific parts of the text using pattern matching
    local patterns = {
      { pattern = "Cloud Status: (.)", hl = hl },
      { pattern = "Personal Domain: (.+)", hl = "NormalFloat" },
      { pattern = "Username: (.+)", hl = "NormalFloat" },
      { pattern = "Email: (.+)", hl = "NormalFloat" },
      { pattern = "Logout", hl = "PiecesUrl" },
    }

    for _, p in ipairs(patterns) do
      local start_pos, end_pos = text:find(p.pattern)
      if start_pos and end_pos then
        if p.pattern == "Cloud Status: (.)" then start_pos = start_pos + #"Cloud Status: " end
        vim.api.nvim_buf_add_highlight(status_popup.bufnr, ns_id, p.hl, i - 1, start_pos - 1, end_pos)
        if p.pattern == "Logout" then
          logout_line = i - 1
        end
      end
    end
  end

  local function handle_click()
    local cursor = vim.api.nvim_win_get_cursor(0)
    local row = cursor[1] - 1
    if row == logout_line then
      vim.cmd('PiecesLogout')
    end
  end
  status_popup:map("n",'<Enter>' , handle_click, { noremap = true })
end

local function login_page()
  local choice = vim.fn.confirm("Note this command only works if you are logged in, Do you want to login?", "&Yes\n&No", 1)
  if choice == 1 then
    vim.cmd("PiecesLogin")
  end
end

local function get_allocation_status()
  local allocation_status = {}

  if user.allocation then
    local status = user.allocation.status
    if status == "PENDING" then
      allocation_status = { { "Cloud Status: • Connecting", "PiecesWarningMsg" } }
    elseif status == "RUNNING" or status == "SUCCEEDED" then
      allocation_status = { { "Cloud Status: • Connected", "PiecesSuccessMsg" } }
    elseif status == "FAILED" then
      allocation_status = { { "Cloud Status: • Disconnected", "PiecesErrorMsg" } }
    end

    if user.url then
      table.insert(allocation_status, { "Personal Domain: " .. user.url, "NormalFloat" })
    end
  else
    if user.is_connecting then
      allocation_status = { { "Cloud Status: Connecting", "PiecesWarningMsg" } }
    else
      allocation_status = { { "Cloud Status: Disconnected", "PiecesErrorMsg" } }
    end
  end

  return allocation_status
end

local function logout_page()
  local allocation_status = get_allocation_status()

  local content = vim.list_extend(
    { { "Username: " .. user.username, "NormalFloat" }, { "Email: " .. user.email, "NormalFloat" } },
    allocation_status
  )
  content = vim.list_extend(content, { { "Logout", "PiecesUrl" } })

  create_ui(content, "NormalFloat")
end

function M.setup()
  if user == nil then
    login_page()
  else
    logout_page()
  end
end

function M.update_user(user_table)
  user = user_table
end

return M
