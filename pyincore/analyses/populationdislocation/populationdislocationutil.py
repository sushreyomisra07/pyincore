"""pyincore.analyses.populationdislocation.populationdislocationutil

Copyright (c) 2017 University of Illinois and others.  All rights reserved.
This program and the accompanying materials are made available under the
terms of the BSD-3-Clause which accompanies this distribution,
and is available at https://opensource.org/licenses/BSD-3-Clause

"""
import pandas as pd


class PopulationDislocationUtil:

    @staticmethod
    def merge_damage_population_block(building_dmg_file, population_allocation_file, block_data_file):
        """Load CSV files to pandas Dataframes, merge them and drop unused columns.

        Args:
            building_dmg_file: A building damage file in csv format.
            population_allocation_file: A population inventory file in csv format.
            block_data_file: A block data file in csv format.

        Returns:
            pd.DataFrame: A merged table of all three inputs.

        """
        # load csv to DataFrame
        building_dmg = pd.read_csv(building_dmg_file)
        population_allocation_inventory = pd.read_csv(population_allocation_file)
        block_data = pd.read_csv(block_data_file)

        damage_states = ["insignific", "moderate", "heavy", "complete"]

        population_allocation_inventory = population_allocation_inventory.drop(columns=damage_states)

        # first merge hazard with popluation allocation inventory on "guid"
        # note guid can be duplicated in population allocation inventory
        df = pd.merge(building_dmg, population_allocation_inventory,
                      how="right", on="guid", validate="1:m")

        # drop columns in building damage that is not used
        df = df.drop(columns=["immocc", "lifesfty", "collprev", "hazardtype",
                              "hazardval", "meandamage",
                              "mdamagedev"])

        # further add block data information to the dataframe
        df["bgid"] = df["blockidstr"].str[1:13].astype(str)
        block_data["bgid"] = block_data["bgid"].astype(str)

        # outer merge on bgid
        final_df = pd.merge(df, block_data, how="outer", on="bgid",
                            validate="m:1")

        return final_df
