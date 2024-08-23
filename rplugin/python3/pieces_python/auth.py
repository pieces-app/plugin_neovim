from ._pieces_lib.pieces_os_client import OSApi,AllocationsApi, UserProfile
from typing import Optional
from .settings import Settings
import concurrent.futures

class Auth:
	user_profile:Optional[UserProfile] = None
	
	@classmethod
	def on_user_callback(cls,user):
		cls.user_profile = user

	def login(self):
		t = OSApi(Settings.api_client).sign_into_os(async_req=True)
		self.print_info(t,"You have been logged in successfully.",
			"Oops! Something went wrong. We could not log you in please try again",self.connect)

	def logout(self):
		t = OSApi(Settings.api_client).sign_out_of_os(async_req=True)
		self.print_info(t, "You have been logged out successfully.",
		 "Oops! Something went wrong. We could not log you out please try again")

	def connect(self):
		user = self.user_profile
		if user: # User logged in
			t = AllocationsApi(Settings.api_client).allocations_connect_new_cloud(user,async_req=True)
			self.print_info(t,"Connected to the personal cloud successfully",
				"Failed to connect from the personal cloud")

	def disconnect(self):
		if self.user_profile and self.user_profile.allocation: # Check if there is an allocation iterable
			t = AllocationsApi(Settings.api_client).allocations_disconnect_cloud(self.user_profile.allocation,async_req=True)
			self.print_info(t,"Disconnected from the personal cloud successfully","Failed to disconnect from the personal cloud")
	
	@staticmethod
	def print_info(thread,failed_message,success_message,on_success=lambda: None):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			future = executor.submit(thread.get, 120)
			try:
				future.result()
				Settings.nvim.out_write(f"{success_message}\n")
				on_success()
			except:
				Settings.nvim.err_write(f"{failed_message}\n")