local function get_os()
	local uv = vim.loop
	local system_name = uv.os_uname().sysname

	if system_name == "Linux" then
		return "LINUX"
	elseif system_name == "Darwin" then
		return "MACOS"
	elseif system_name == "Windows" then
		return "WINDOWS"
	else
		return "UNKNOWN"
	end
end

-- All user configration should be here for the user to config
local config = {}

config.os = get_os()



return config 
