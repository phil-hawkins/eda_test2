import json
import os
from pathlib import Path
from dataclasses import asdict, dataclass


@dataclass
class Config:
    SETTINGS_REL_PATH = ".vscode/settings.json"
    SQLTOOLS_KEY = "sqltools.connections"
    SQLTOOLS_USERNAME_KEY = "username"
    USERNAME_ENV_KEY = "NIB_USERNAME"


@dataclass
class SnowflakeConnectionConfig:
    authenticator: str = "externalbrowser"
    warehouse: str = "group_general"
    database: str = "build_prod"
    role: str = "nib_dwh"
    account: str = "ly01550.ap-southeast-2"
    ocsp_fail_open: bool = True
    sqltools_connection_config = [
        {
            "authenticator": authenticator,
            "ocspOptions": {"ocspFailOpen": ocsp_fail_open},
            "snowflakeOptions": {
                "clientSessionKeepAlive": True,
                "clientSessionKeepAliveHeartbeatFrequency": 3600,
                "role": role,
            },
            "previewLimit": 50,
            "driver": "Snowflake",
            "username": "",
            "name": database,
            "database": database,
            "account": account,
            "warehouse": warehouse,
        }
    ]


class VSCodeSettings:
    def __init__(self) -> None:
        self._config = Config()

        # find the settings file
        test_path = Path(".").absolute()
        self._settings_path = None
        if test_path.joinpath(self._config.SETTINGS_REL_PATH).is_file():
            self._settings_path = test_path.joinpath(self._config.SETTINGS_REL_PATH)
        else:
            while test_path != test_path.parent:
                test_path = test_path.parent
                if test_path.joinpath(self._config.SETTINGS_REL_PATH).is_file():
                    self._settings_path = test_path.joinpath(
                        self._config.SETTINGS_REL_PATH
                    )

        # load settings
        if self._settings_path is None:
            raise FileNotFoundError(
                f"Could not find {self._config.SETTINGS_REL_PATH} in any parent directory."
            )
        else:
            with open(self._settings_path, "r") as settings_file:
                self._settings = json.load(settings_file)

        # get the username
        self._username = self._get_sfuser_from_env()
        if self._username is None:
            self._username = self._get_sfuser_from_settings()
        if self._username is None:
            raise RuntimeError(
                "Could not find user name from environment var or settings.json"
            )

    def set_sqltools_username(self, username: str = None) -> None:
        username = self._username if username is None else username

        for connection in self._settings[self._config.SQLTOOLS_KEY]:
            connection[self._config.SQLTOOLS_USERNAME_KEY] = username

    def sqltools_config_exists(self) -> bool:
        return self._settings.get(self._config.SQLTOOLS_KEY) is not None

    def set_sqltools_default(self) -> None:
        self._settings[
            self._config.SQLTOOLS_KEY
        ] = SnowflakeConnectionConfig().sqltools_connection_config

    def save(self) -> None:
        with open(self._settings_path, "w") as settings_file:
            json.dump(self._settings, settings_file, indent=4)

    def _get_sfuser_from_env(self) -> str:
        return os.environ.get(self._config.USERNAME_ENV_KEY)

    def _get_sfuser_from_settings(self) -> str:
        """get the username from the first snowfloke connection in settings.json

        returns: (str) the full nib username or None if no connection config exists
        """
        sfuser = None
        connectionss_config = self._settings.get(self._config.SQLTOOLS_KEY)
        if connectionss_config and (len(connectionss_config) >= 1):
            sfuser = connectionss_config[0].get(self._config.SQLTOOLS_USERNAME_KEY)

        return sfuser

    def get_snowflake_connection_config(
        self, database: str = None, schema: str = None
    ) -> dict:
        connection_config = asdict(SnowflakeConnectionConfig())
        connection_config["user"] = self._username
        if database is not None:
            connection_config["database"] = database
        if schema is not None:
            connection_config["schema"] = schema

        return connection_config
