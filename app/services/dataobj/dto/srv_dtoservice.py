from pathlib import Path
from typing import Any

from app.config import get_settings
from app.services.dataobj.watcher.srv_watcher import FileWatcher
from loguru import logger
from src.domain.digipos.rep_digipos import DigiposProductRepository
from src.domain.member.rep_member import MemberRepository
from src.domain.module.rep_module import ModuleRepository

MEMBERS_YAML = "members.yaml"
MODULES_YAML = "modules.yaml"
DGPRODUCTS_YAML = "digipos.yaml"


class DataService:
    """Service to manage data repositories and file watchers.

    Easily extensible for new repositories and watchers.
    """

    def __init__(self) -> None:
        self.data_path = Path(get_settings().APP.datapath).resolve()
        self.repos: dict[str, Any] = {}
        self.watchers: dict[str, FileWatcher] = {}
        self._init_repositories()
        self._init_watchers()

    def _init_repositories(self) -> None:
        """Initialize all repositories."""
        self.repos["member"] = MemberRepository(self.data_path / MEMBERS_YAML)
        logger.info("MemberRepository initialized")

        self.repos["module"] = ModuleRepository(self.data_path / MODULES_YAML)
        logger.info("ModuleRepository initialized")

        self.repos["digipos"] = DigiposProductRepository(
            self.data_path / DGPRODUCTS_YAML
        )
        logger.info("DigiposProductRepository initialized")
        # Add more repositories here as needed

    def _init_watchers(self) -> None:
        """Initialize all file watchers."""
        self.watchers["member"] = FileWatcher(
            self.data_path / MEMBERS_YAML, self.repos["member"].reload
        )
        logger.info(
            "Member FileWatcher initialized", path=str(self.data_path / MEMBERS_YAML)
        )
        self.watchers["module"] = FileWatcher(
            self.data_path / MODULES_YAML, self.repos["module"].reload
        )
        logger.info(
            "Module FileWatcher initialized", path=str(self.data_path / MODULES_YAML)
        )
        self.watchers["digipos"] = FileWatcher(
            self.data_path / DGPRODUCTS_YAML, self.repos["digipos"].reload
        )
        logger.info(
            "Digipos FileWatcher initialized",
            path=str(self.data_path / DGPRODUCTS_YAML),
        )
        # Add more watchers here as needed

    def start(self) -> None:
        """Start all watchers."""
        for name, watcher in self.watchers.items():
            try:
                watcher.start()
                logger.info(f"{name.capitalize()} watcher started")
            except Exception as e:
                logger.error(f"Failed to start {name} watcher", error=str(e))

    def stop(self) -> None:
        """Stop all watchers."""
        for name, watcher in self.watchers.items():
            try:
                watcher.stop()
                logger.info(f"{name.capitalize()} watcher stopped")
            except Exception as e:
                logger.error(f"Failed to stop {name} watcher", error=str(e))

    def start_all(self) -> None:
        """Start all file watchers."""
        for name, watcher in self.watchers.items():
            try:
                watcher.start()
                logger.info(f"Started watcher: {name}")
            except Exception as e:
                logger.error(f"Failed to start watcher: {name}", error=str(e))

    def stop_all(self) -> None:
        """Stop all file watchers."""
        for name, watcher in self.watchers.items():
            try:
                watcher.stop()
                logger.info(f"Stopped watcher: {name}")
            except Exception as e:
                logger.error(f"Failed to stop watcher: {name}", error=str(e))
        logger.info("All watchers stopped")

    @property
    def member_repo(self) -> MemberRepository:
        return self.repos["member"]

    @property
    def module_repo(self) -> ModuleRepository:
        return self.repos["module"]

    @property
    def digipos_repo(self) -> DigiposProductRepository:
        return self.repos["digipos"]

    # Just For Ease Of Accsess
    def get_repo(self, name: str) -> Any:
        """Get repository by name (generic accessor)."""
        return self.repos.get(name)

    def reload_all(self) -> None:
        """Reload all repositories that have a reload method."""
        for name, repo in self.repos.items():
            if hasattr(repo, "reload") and callable(repo.reload):
                try:
                    repo.reload()
                    logger.info(
                        f"Reloaded repository: {name} ({repo.__class__.__name__})"
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to reload repository: {name} ({repo.__class__.__name__})",
                        error=str(e),
                    )
            else:
                logger.warning(
                    f"Repository {name} ({repo.__class__.__name__}) has no reload method"
                )
