# Helper functions
from app.schemas.auth_schema import DeviceInfo
from user_agents import parse

class Helpers:
    @staticmethod
    def get_device_info(user_agent: str) -> DeviceInfo:
        user_agent = parse(user_agent)
        return DeviceInfo(
            os=user_agent.os.family,
            os_version=user_agent.os.version_string,
            browser=user_agent.browser.family,
            browser_version=user_agent.browser.version_string,
            device=user_agent.device.family,
            is_mobile=user_agent.is_mobile,
            is_tablet=user_agent.is_tablet,
            is_pc=user_agent.is_pc,
        )