"""Module for connecting to and managing Notion databases."""
import os
from typing import Any
from notion_client import Client, AsyncClient
from nuploaders import log


class NotionConnectClient:
    """Handles Notion API client connections."""

    def __init__(self):
        notion_token = os.getenv("NOTION_TOKEN")
        self.single_notion = Client(auth=notion_token)
        self.notion = AsyncClient(auth=notion_token)


class NotionDBManager(NotionConnectClient):
    """Provides helpers to create and populate Notion databases."""

    def _make_db_properties(self, column_name_property: dict) -> dict[str, Any]:
        """
        Create Notion database properties based on column types.

        Args:
            column_name_property: Mapping of column names to metadata.

        Returns:
            dict[str, Any]: Formatted Notion property definitions.
        """
        property_dict = {}
        is_first_key = True
        for key in column_name_property:
            col_type = column_name_property[key]["type"]
            options = column_name_property[key].get("col_options", [])
            if is_first_key:
                property_dict[key] = {"title": {}}
                is_first_key = False
            elif col_type == "string":
                property_dict[key] = self._get_static_template_rich_text()
            elif col_type == "boolean":
                property_dict[key] = self._get_static_template_checkbox()
            elif col_type == "single_category":
                property_dict[key] = self._get_static_template_select(options)
            elif col_type == "multi_category":
                property_dict[key] = self._get_static_template_multi_select(options)
            elif col_type == "people":
                property_dict[key] = self._get_static_template_multi_people()
            elif col_type == "link":
                property_dict[key] = self._get_static_template_url()
            else:
                raise ValueError("number, files are yet to be implemented")
        return property_dict

    def _convert_datype_ntype(self, datatype: str) -> str:
        notion_datatypes = {
            "string": "rich_text",
            "boolean": "checkbox",
            "single_category": "select",
            "multi_category": "multi_select",
            "people": "people",
            "attachment": "files",
            "int": "number",
            "float": "number"
        }
        return notion_datatypes.get(datatype, "rich_text")

    def _get_static_template_rich_text(self, update=False, val=None) -> dict[str, Any]:
        if update:
            return {"rich_text": [{"text": {"content": val}}]}
        return {"rich_text": {}}

    def _get_static_template_checkbox(self, update=False, val=None) -> dict[str, Any]:
        if update:
            return {"checkbox": val}
        return {"checkbox": False}

    def _get_static_template_select(
        self, col_options, update=False, val=None
    ) -> dict[str, Any]:
        if update:
            return {"select": {"name": val}}
        return {"select": {"options": col_options}}

    def _get_static_template_number(self, update=False, val=None) -> dict[str, Any]:
        if update:
            return {"number": float(val)}
        return {"number": {"format": "dollar"}}

    def _get_static_template_multi_select(
        self, col_options, update=False, val=None
    ) -> dict[str, Any]:
        if update:
            return {"multi_select": [{"name": v} for v in val]}
        return {"multi_select": {"options": col_options}}

    def _get_static_template_url(self, update=False, val=None) -> dict[str, Any]:
        if update:
            return {"url": val}
        return {"url": {}}

    def _get_static_template_multi_people(self, update=False, val=None) -> dict[str, Any]:
        if update:
            return {"people": val}
        return {"people": []}

    def _make_db_title(self, db_name=None, update=False, val=None) -> list:
        if update:
            return {"title": [{"text": {"content": val}}]}
        return [{"type": "text", "text": {"content": db_name}}]

    def _set_db_icon(self, icon, update=False) -> dict[str, Any]:
        return {"type": "emoji", "emoji": icon}

    def _set_db_parent(self, parent_page_id: str) -> dict[str, Any]:
        return {"type": "page_id", "page_id": parent_page_id}

    def create_database(
        self, parent_page_id: str, db_name: str, column_name_property: dict, page_title_icon=None
    ) -> str:
        """
        Create a Notion database.

        Args:
            parent_page_id (str): The ID of the parent page.
            db_name (str): Name of the new database.
            column_name_property (dict): Property structure of the database.
            page_title_icon (str): Optional emoji icon.

        Returns:
            str: The created database object.
        """
        log.info("creating a database %s under parent page %s", db_name, parent_page_id)
        properties = self._make_db_properties(column_name_property)
        title = self._make_db_title(db_name)
        icon = self._set_db_icon(page_title_icon)
        parent = self._set_db_parent(parent_page_id)
        newdb = self.single_notion.databases.create(
            parent=parent, title=title, properties=properties, icon=icon
        )
        return newdb

    async def write_to_database(self, row, database_id):
        """
        Write a single row to the specified Notion database.

        Args:
            row (dict): Data row to insert.
            database_id (str): Target Notion database ID.
        """
        log.info("Inserting into database_id %s", database_id)
        return await self.notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "title": self._make_db_title(val=row["title"], update=True),
                "enrich_mycategory": self._get_static_template_rich_text(
                    val=row["enrich_mycategory"], update=True
                ),
                "genre": self._get_static_template_rich_text(val=row["genre"], update=True),
                "imdbid": self._get_static_template_rich_text(val=row["imdbid"], update=True),
                "imdblink": self._get_static_template_url(val=row["imdblink"], update=True),
                "imdbrating": self._get_static_template_rich_text(
                    val=row["imdbrating"], update=True
                ),
                "ratings": self._get_static_template_rich_text(val=row["ratings"], update=True),
                "runtime": self._get_static_template_rich_text(val=row["runtime"], update=True),
            },
        )
