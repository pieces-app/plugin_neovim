from ._pieces_lib.pieces_os_client import UserProfile
from typing import Optional
from .settings import Settings
import concurrent.futures
from .utils import convert_to_lua_table

class Auth:
	user_profile:Optional[UserProfile] = None
	
	@classmethod
	def on_user_callback(cls,user:Optional[UserProfile]):
		cls.user_profile = user
		if not user:
			cls.send_lua()
		else:
			cls.send_lua(cls.get_compact_dict(cls.user_profile))
		

	@staticmethod
	def send_lua(python_dict=None):
		lua_str = "nil"
		if python_dict:
			lua_str = convert_to_lua_table(python_dict)
		Settings.nvim.async_call(Settings.nvim.exec_lua,f"require('pieces.auth').update_user({lua_str})")

	@staticmethod
	def get_compact_dict(user):
		# Updating lua cache
		lua_out = {
			"username":user.name or user.username,
			"email":user.email
		}
		allocation = user.allocation
		if allocation:
			status = allocation.status.cloud
			lua_out["allocation"] = {"status":status.value}
			if allocation.urls.vanity:
				url = allocation.urls.vanity.url
				lua_out["url"] = url
		return lua_out


	def login(self,show_ui=False):
		def on_login_success():
			Settings.nvim.command("PiecesAccount")
			self.connect()
		callback = on_login_success if show_ui else lambda:None
		t = Settings.api_client.os_api.sign_into_os(async_req=True)
		self.print_info(t,"You have been logged in successfully.",
			"Oops! Something went wrong. We could not log you in please try again",callback)

	def logout(self):
		t = Settings.api_client.os_api.sign_out_of_os(async_req=True)
		self.print_info(t, "You have been logged out successfully.",
		 "Oops! Something went wrong. We could not log you out please try again")

	def connect(self):
		user = self.user_profile
		if not user:
			return Settings.nvim.err_write("You must be logged in to use this feature\n")
		compact = self.get_compact_dict(user)
		compact["is_connecting"] = True
		self.send_lua(compact)
		t = Settings.api_client.allocations_api.allocations_connect_new_cloud(user,async_req=True)
		self.print_info(t,"Connected to the personal cloud successfully",
			"Failed to connect from the personal cloud")

	def disconnect(self):
		if not self.user_profile:
			return Settings.nvim.err_write("You must be logged in to use this feature\n")
		if self.user_profile.allocation: # Check if there is an allocation iterable
			t = Settings.api_client.allocations_api.allocations_disconnect_cloud(self.user_profile.allocation,async_req=True)
			self.print_info(t,"Disconnected from the personal cloud successfully","Failed to disconnect from the personal cloud")
	
	@staticmethod
	def print_info(thread,success_message,failed_message,on_success=lambda: None):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			future = executor.submit(thread.get, 120)
			try:
				future.result()
				Settings.nvim.out_write(f"{success_message}\n")
				on_success()
			except:
				Settings.nvim.err_write(f"{failed_message}\n")

