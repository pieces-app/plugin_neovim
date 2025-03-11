local ListUpdater = {}
ListUpdater.__index = ListUpdater

-- Constructor for ListUpdater
function ListUpdater:new(
	results_popup,
	current_index,
	items,
	get_base_name,
	get_annotation,
	enter_keymap,
	delete_keymap,
	on_update,
	multi_select,
	get_unique_id
) -- Optional function to get unique identifier
	local instance = {
		results_popup = results_popup,
		current_index = current_index,
		items = items,
		get_base_name = get_base_name,
		get_annotation = get_annotation,
		get_unique_id = multi_select and get_unique_id or nil, -- Store the function only if multi_select is true
		enter_keymap = enter_keymap,
		delete_keymap = delete_keymap,
		on_update = on_update,
		multi_select = multi_select or false,
		selected_items = {},
	}
	setmetatable(instance, ListUpdater)
	return instance
end

function ListUpdater:_update_list_common()
	if
		self.results_popup == nil
		or type(self.results_popup.bufnr) ~= "number"
		or not vim.api.nvim_buf_is_valid(self.results_popup.bufnr)
	then
		return
	end

	local lines = {}
	local end_col, start_col, annotation_index

	for i, item in ipairs(self.items) do
		local base_name = self.get_base_name(item)
		local prefix = " "
		local unique_id = self.multi_select and self.get_unique_id(item) or nil -- Get the unique identifier only if multi_select is true

		if self.multi_select and self.selected_items[unique_id] then
			prefix = "*"
		elseif i == self.current_index then
			prefix = ">"
		end

		if i == self.current_index then
			-- Highlighted line (current selection)
			local highlighted_line = prefix .. " " .. base_name .. " "
			local annotation = self.get_annotation(item):gsub("\n", " ")
			start_col = #highlighted_line
			highlighted_line = highlighted_line .. annotation
			end_col = start_col + #annotation
			annotation_index = i - 1 -- Convert to 0-based index for highlighting
			table.insert(lines, highlighted_line)
		else
			table.insert(lines, prefix .. " " .. base_name)
		end
	end

	vim.api.nvim_buf_set_lines(self.results_popup.bufnr, 0, -1, false, lines)

	-- Apply the highlight if annotation_index is valid
	if annotation_index then
		vim.api.nvim_buf_add_highlight(
			self.results_popup.bufnr,
			-1,
			"PiecesAnnotation",
			annotation_index,
			start_col,
			end_col
		)
	end

	local win_height = vim.api.nvim_win_get_height(self.results_popup.winid) - 5 -- Removing the borders
	local cursor_line = self.current_index - 1 -- Convert to 0-based index for nvim_win_set_cursor
	if cursor_line >= win_height or cursor_line - win_height < 0 then
		vim.api.nvim_win_set_cursor(self.results_popup.winid, { self.current_index, 0 })
	end
end

function ListUpdater:update()
	self:_update_list_common()
	if type(self.on_update) == "function" then
		self.on_update(self)
	end
end

function ListUpdater:down_keymap()
	if self.current_index < #self.items then
		self.current_index = self.current_index + 1
		self:update()
	end
end

function ListUpdater:up_keymap()
	if self.current_index > 1 then
		self.current_index = self.current_index - 1
		self:update()
	end
end

function ListUpdater:toggle_selection()
	if self.multi_select then
		local unique_id = self.get_unique_id(self.items[self.current_index])
		self.selected_items[unique_id] = not self.selected_items[unique_id]
		self:update()
	end
end

function ListUpdater:setup_keymaps()
	local keymaps = {
		["<Up>"] = function()
			self:up_keymap()
		end,
		["<Down>"] = function()
			self:down_keymap()
		end,
		["k"] = function()
			self:up_keymap()
		end,
		["j"] = function()
			self:down_keymap()
		end,
		["<esc>"] = function()
			self.results_popup:unmount()
		end,
		["<C-c>"] = function()
			self.results_popup:unmount()
		end,
		["<enter>"] = function()
			self.enter_keymap(self.items[self.current_index])
		end,
		["<Del>"] = function()
			self.delete_keymap(self.items[self.current_index])
		end,
		["<kDel>"] = function()
			self.delete_keymap(self.items[self.current_index])
		end,
		["<BS>"] = function()
			self.delete_keymap(self.items[self.current_index])
		end,
		["<C-d>"] = function()
			self.delete_keymap(self.items[self.current_index])
		end,
	}
	local modes = { "i", "n" }

	for key, func in pairs(keymaps) do
		for _, mode in ipairs(modes) do
			self.results_popup:map(mode, key, func, { noremap = true })
		end
	end
end

function ListUpdater:setup()
	self:setup_keymaps()
	self:update()
end

function ListUpdater:mount()
	self.results_popup:mount()
	vim.api.nvim_set_current_win(self.results_popup.winid)
	self:setup()
end

return ListUpdater
