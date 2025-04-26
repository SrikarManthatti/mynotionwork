import os
from typing import Any
from notion_client import Client
from nuploaders import log

class NotionConnectClient():
    def __init__(self):
        NOTION_TOKEN = os.getenv("NOTION_TOKEN")
        self.notion = Client(auth = NOTION_TOKEN)

class NotionDBManager(NotionConnectClient):
    def _make_db_properties(self, column_name_property: dict) -> dict[str, Any]:
        """This will be used to create properties for db, column name and type of columns"""
        #{"cola":{"type":"string","col_options":[]}}
        property_dict = {}
        is_first_key = True
        for key in column_name_property.keys():
            if is_first_key:
                property_dict[key] = {"title": {}} #mandatory for notion db, hence making the first key/column as title
                is_first_key = False
            else:
                if column_name_property[key]["type"] == "string":
                    property_dict[key] = self._get_static_template_rich_text()
                elif column_name_property[key]["type"] == "boolean":
                    property_dict[key] = self._get_static_template_checkbox()
                elif column_name_property[key]["type"] == "single_category":
                    property_dict[key] = self._get_static_template_select(column_name_property[key]["col_options"])
                elif column_name_property[key]["type"] == "multi_category":
                    property_dict[key] = self._get_static_template_multi_select(column_name_property[key]["col_options"])
                elif column_name_property[key]["type"] == "people":
                    property_dict[key] = self._get_static_template_multi_people() 
                else:
                    #log.warn("number, files are yet to be implemented")
                    raise ValueError("number, files are yet to be implemented")
        return property_dict
        
    def _convert_datype_ntype(self, datatype: str) -> str:
        notion_datatypes = {"string": "rich_text", "boolean": "checkbox", "single_category": "select", "multi_category": "multi_select", "people": "people", "attachment": "files", "int": "number", "float": "number"}
        return notion_datatype.get(datatype, "rich_text")
    
    def _get_static_template_rich_text(self) -> dict[str, Any]:
        return {"rich_text": {}}
    
    def _get_static_template_checkbox(self) -> dict[str, Any]:
        return {"checkbox": {}}
    
    def _get_static_template_select(self,col_options) -> dict[str, Any]:
        return {"select": {"options": col_options}}
    
    def _get_static_template_number(self) -> dict[str, Any]:
        return {"number": {"format": "dollar"}}
    
    def _get_static_template_multi_select(self, col_options) -> str:
        return {"type": "multi_select","multi_select": {"options": col_options},}
    
    
    def _make_db_title(self, db_name: str) -> list:
        """This will be used to create title property for db"""
        return [{"type": "text", "text": {"content": db_name}}]
    
    def _set_db_icon(self, icon) -> dict[str, Any]:
        return {"type": "emoji", "emoji": icon}

    def _set_db_parent(self, parent_page_id: str) -> dict[str, Any]:
        return {"type": "page_id", "page_id": parent_page_id}
    
    def create_database(self, parent_page_id: str, db_name: str, column_name_property: dict,  page_title_icon = None) -> str:
        """This function will be used to create database under a parent page"""
        log.info("creating a database %s under parent page %s", db_name, parent_page_id)
        properties = self._make_db_properties(column_name_property)
        title = self._make_db_title(db_name)
        icon = self._set_db_icon(page_title_icon)
        parent = self._set_db_parent(parent_page_id)
        return self.notion.databases.create(parent=parent, title=title, properties=properties, icon=icon)









