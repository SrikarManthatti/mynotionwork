import os
from typing import Any
from notion_client import Client

class NotionConnectClient():
    def __init__(self):
        NOTION_TOKEN = os.getenv("NOTION_TOKEN")
        self.notion = Client(auth = NOTION_TOKEN)

class NotionDBManager(NotionConnectClient):
    def _make_db_properties(column_name_property: dict) -> dict[str, Any]:
        """This will be used to create properties for db, column name and type of columns"""
        pass #todo need to create a logic to write a dict that will generate column name with properties 
    
    def _convert_datype_ntype(datatype: str) -> str:
        notion_datatypes = {"string": "rich_text", "boolean": "checkbox", "single_category": "select", "multi_category": "multi_select", "people": "people", "attachment": "files", "int": "number", "float": "number"}
        return notion_datatype.get(datatype, "rich_text")
    
    def _get_static_template_rich_text(col_name) -> dict[str, Any]:
        return {col_name: {"rich_text": {}}}
    
    def _get_static_template_checkbox(col_name) -> dict[str, Any]:
        return {col_name: {"checkbox": {}}}
    
    def _get_static_template_select(col_name, col_options) -> dict[str, Any]:
        return {col_name: {"select": {"options": col_options}}}
    
    def _get_static_template_number(col_name) -> dict[str, Any]:
        return {col_name: {"number": {"format": "dollar"}}}
    
    def _get_static_template_multi_select(col_name, col_options) -> str:
        return {col_name: {"type": "multi_select","multi_select": {"options": col_options},}}
    
    
    def _make_db_title(db_name: str) -> list:
        """This will be used to create title property for db"""
        return [{"type": "text", "text": {"content": db_name}}]
    
    def _set_db_icon(icon) -> dict[str, Any]:
        return {"type": "emoji", "emoji": icon}

    def _set_db_parent(parent_page_id: str) -> dict[str, Any]:
        return {"type": "page_id", "page_id": parent_page_id}
    
    def create_database(self, parent_page_id: str, db_name: str, column_name_property: dict,  page_title_icon = None) -> str:
        """This function will be used to create database under a parent page"""
        log.info("creating a database %s under parent page %s", db_name, parent_page_id)
        properties = _make_db_properties(column_name_property)
        title = _make_db_title(db_name)
        icon = _set_db_icon(page_title_icon)
        parent = _set_db_parent(parent_page_id)
        return self.notion.databases.create(parent=parent, title=title, properties=properties, icon=icon)









