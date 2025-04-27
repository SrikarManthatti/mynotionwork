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
                elif column_name_property[key]["type"] == "link":
                    property_dict[key] = self._get_static_template_url()
                else:
                    #log.warn("number, files are yet to be implemented")
                    raise ValueError("number, files are yet to be implemented")
        return property_dict
        
    def _convert_datype_ntype(self, datatype: str) -> str:
        notion_datatypes = {"string": "rich_text", "boolean": "checkbox", "single_category": "select", "multi_category": "multi_select", "people": "people", "attachment": "files", "int": "number", "float": "number"}
        return notion_datatype.get(datatype, "rich_text")
    
    def _get_static_template_rich_text(self, update = False, val = None) -> dict[str, Any]:
        if update:
            return {"rich_text": [{"text": {"content": val}}]}
        else:
            return {"rich_text": {}}
    
    def _get_static_template_checkbox(self, update = False, val = None) -> dict[str, Any]:
        if update:
            return {"checkbox": [{"text": {"content": val}}]}
        else:
            return {"checkbox": {}}
    
    def _get_static_template_select(self,col_options, update = False, val = None) -> dict[str, Any]:
        if update:
            return {"select": {"name": val}}
        else:
            return {"select": {"options": col_options}}
    
    def _get_static_template_number(self, update = False, val = None) -> dict[str, Any]:
        if update:
            return {"number": float(val)}
        else:
            return {"number": {"format": "dollar"}}
    
    def _get_static_template_multi_select(self, col_options, update = False, val = None) -> str:
        if update:
            return {"multi_select": {"name": val}}
        else:
            return {"type": "multi_select","multi_select": {"options": col_options},}
    
    
    def _get_static_template_url(self, update = False, val = None) -> str:
        if update:
            return {"url": val}
        else:
            return {"url": {}}

    def _make_db_title(self, db_name = None, update = False, val = None) -> list:
        """This will be used to create title property for db"""
        if update:
            return {"title": [{"text": {"content": val}}]}
        else:
            return [{"type": "text", "text": {"content": db_name}}]
    
    def _set_db_icon(self, icon, update = False) -> dict[str, Any]:
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
        newdb = self.notion.databases.create(parent=parent, title=title, properties=properties, icon=icon)
        return newdb
    
    def write_to_database(self, row, database_id):
        "this will write each row to db in notion"
        log.info("Inserting into database_id %s", database_id)
        return self.notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "title": self._make_db_title(val = row['title'], update = True),
            "enrich_mycategory": self._get_static_template_rich_text(val = row['enrich_mycategory'], update = True),
            "genre": self._get_static_template_rich_text(val = row['genre'], update = True),
            "imdbid": self._get_static_template_rich_text(val = row['imdbid'], update = True),
            "imdblink": self._get_static_template_url(val = row['imdblink'], update = True),
            "imdbrating": self._get_static_template_rich_text(val = row['imdbrating'], update = True),
            "ratings": self._get_static_template_rich_text(val = row['ratings'], update = True),
            "runtime": self._get_static_template_rich_text(val = row['runtime'], update = True),
        }
    )









