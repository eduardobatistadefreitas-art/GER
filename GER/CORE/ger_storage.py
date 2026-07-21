"""
============================================================
GER CORE

Storage

GER — Geometria Espectral Relacional
============================================================

Infraestrutura padrão para armazenamento dos experimentos.

Responsabilidades

• Detectar o Google Drive
• Criar automaticamente a estrutura do experimento
• Fornecer objetos Path
• Padronizar o armazenamento do GER

============================================================
"""

from __future__ import annotations

from pathlib import Path


class ExperimentStorage:

    """
    Gerencia o armazenamento persistente dos experimentos.
    """

    ROOT = Path(
        "/content/drive/MyDrive/GER_RESULTS"
    )

    # --------------------------------------------------------

    def __init__(

        self,

        experiment: str,

        folders=None,

        verbose=True,

    ):

        self.experiment = experiment

        self.verbose = verbose

        self.folders_map = {}

        if folders is None:

            folders = []

        self._initialize(folders)

    # --------------------------------------------------------

    def _initialize(

        self,

        folders,

    ):

        if not self.ROOT.exists():

            raise RuntimeError(

                "\nGoogle Drive not mounted.\n"
                "Mount Google Drive before running this experiment."

            )

        self.database = (

            self.ROOT

            /

            self.experiment

        )

        self.database.mkdir(

            parents=True,

            exist_ok=True,

        )

        for name in folders:

            path = (

                self.database

                /

                name

            )

            path.mkdir(

                parents=True,

                exist_ok=True,

            )

            self.folders_map[name] = path

        if self.verbose:

            self._print_summary()

    # --------------------------------------------------------

    def _print_summary(self):

        print("=" * 60)
        print("Persistent Storage")
        print("=" * 60)
        print("[OK] Google Drive")
        print(f"[OK] Output : {self.database}")
        print("=" * 60)

    # --------------------------------------------------------

    @property
    def root(self):

        return self.ROOT

    # --------------------------------------------------------

    def folder(

        self,

        name,

    ):

        if name not in self.folders_map:

            raise KeyError(

                f"Folder '{name}' was not registered."

            )

        return self.folders_map[name]

    # --------------------------------------------------------

    def file(

        self,

        folder,

        filename,

    ):

        return (

            self.folder(folder)

            /

            filename

        )

    # --------------------------------------------------------

    def create_folder(

        self,

        name,

    ):

        if name in self.folders_map:

            return self.folders_map[name]

        path = (

            self.database

            /

            name

        )

        path.mkdir(

            parents=True,

            exist_ok=True,

        )

        self.folders_map[name] = path

        return path

    # --------------------------------------------------------

    def exists(

        self,

        folder,

        filename,

    ):

        return self.file(

            folder,

            filename,

        ).exists()

    # --------------------------------------------------------

    def list_folders(self):

        return sorted(

            self.folders_map.keys()

        )

    # --------------------------------------------------------

    def list_files(

        self,

        folder,

    ):

        return sorted(

            p.name

            for p in self.folder(folder).iterdir()

            if p.is_file()

        )

    # --------------------------------------------------------

    def __repr__(self):

        return (

            f"ExperimentStorage("
            f"experiment='{self.experiment}'"
            f")"

        )
