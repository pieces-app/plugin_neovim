local Popup = require('nui.popup')
local ListUpdater = require("pieces.list_updater")
local make_buffer_read_only = require("pieces.utils").make_buffer_read_only
local M = {}
local results_popup,updater
local path = require("pieces.copilot.context.paths")
local assets = require("pieces.copilot.context.assets")

local annotations = {
	Folders="Add local code repositories and folders as context for your Copilot",
	Files="qGPT uses local code files to find code that's relevant to your Copilot questions",
	Snippets="Save a Snippet to use as context for your Copilot",
}

local function on_enter(item)
	results_popup:unmount()
	if item == "Files" or item == "Folders" then
		return path.setup(item)
	else
		assets.setup()
	end
end

updater = ListUpdater:new(results_popup,
	1, {"Files","Folders","Snippets"},
	function (item)
		return item
	end,
	function (item)
		return annotations[item]
	end,
	on_enter,
	function (item) end)

function M.setup()
	-- Create the results popup
	results_popup = Popup({
		relative = "editor",
		position = "50%",
		size = {
			width = "60%",
			height = 5,
		},
		border = {
			style = "rounded",
			text = {
				top = " Add Context ",
				top_align = "center",
			},
		},
		win_options = {
			winhighlight = "Normal:Normal,FloatBorder:FloatBorder",
		},
	})
	make_buffer_read_only(results_popup.bufnr)
	updater.results_popup = results_popup -- Update the new result popup
	updater:mount()
end

return M
