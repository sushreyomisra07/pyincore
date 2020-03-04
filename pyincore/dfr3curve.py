# Copyright (c) 2019 University of Illinois and others. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License v2.0 which accompanies this distribution,
# and is available at https://www.mozilla.org/en-US/MPL/2.0/


import json

from pyincore.dfr3service import Dfr3Service


class DFR3Curves:
    """class for dfr3 curves.

    Args:
        metadata (dict): dfr3 curve metadata.

    """

    def __init__(self, metadata):
        self.id = metadata["id"]
        self.demand_type = metadata["demandType"]
        self.demand_units = metadata["demandUnits"]
        self.result_type = metadata["resultType"]
        self.hazard_type = metadata['hazardType']
        self.inventory_type = metadata['inventoryType']
        # TODO need to represent fragility curves better
        self.fragility_curves = metadata["fragilityCurve"]

    @classmethod
    def from_dfr3_service(cls, id: str, dfr3_service: Dfr3Service):
        """Get an dfr3set object from dfr3 services.

        Args:
            id:
            dfr3_service:

        Returns:
            obj: dfr3set from dfr3 service.

        """
        metadata = Dfr3Service.get_dfr3_set(id)
        instance = cls(metadata)

        return instance

    @classmethod
    def from_json_str(cls, json_str):
        """Get dfr3set from json string.

        Args:
            json_str (str): JSON of the Dataset.

        Returns:
            obj: dfr3set from JSON.

        """
        return cls(json.loads(json_str))

    @classmethod
    def from_json_file(cls, file_path):
        """Get dfr3set from the file.

        Args:
            file_path (str): json file path that holds the definition of a dfr3 curve.

        Returns:
            obj: dfr3set from file.

        """
        with open(file_path, "w") as f:
            instance = cls(json.load(f))

        return instance
