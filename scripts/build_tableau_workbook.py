#!/usr/bin/env python3
"""Build and validate genuine Tableau workbook (.twb and .twbx) for EV Market Intelligence."""
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd
from tableaudocumentapi import Workbook

WORKSPACE = Path(r"D:\EV_Tableau_Project_Starter_Kit")
CSV_PATH = WORKSPACE / "data" / "ev_market_clean.csv"
TWB_PATH = WORKSPACE / "tableau" / "EV_Market_Intelligence.twb"
TWBX_PATH = WORKSPACE / "tableau" / "EV_Market_Intelligence.twbx"

# Read columns and determine types
df = pd.read_csv(CSV_PATH, nrows=5)
col_defs = []
for i, col in enumerate(df.columns):
    dtype = str(df[col].dtype)
    if 'int' in dtype:
        t = 'integer'
    elif 'float' in dtype:
        t = 'real'
    else:
        t = 'string'
    col_defs.append((i, col, t))

def build_twb_xml(csv_rel_dir="../data", csv_filename="ev_market_clean.csv"):
    # Build column XML tags
    cols_xml = []
    metadata_xml = []
    for ord_idx, name, dtype in col_defs:
        cols_xml.append(f'            <column datatype=\'{dtype}\' name=\'[{name}]\' ordinal=\'{ord_idx}\' />')
        metadata_xml.append(f'''          <metadata-record class=\'column\'>
            <remote-name>{name}</remote-name>
            <remote-type>{129 if dtype=="string" else (20 if dtype=="integer" else 5)}</remote-type>
            <local-name>[{name}]</local-name>
            <parent-name>[ev_market_clean.csv]</parent-name>
            <remote-alias>{name}</remote-alias>
            <ordinal>{ord_idx}</ordinal>
            <local-type>{dtype}</local-type>
            <aggregation>{'Count' if dtype=="string" else 'Sum'}</aggregation>
            <scale>1</scale>
            <width>255</width>
            <contains-null>true</contains-null>
          </metadata-record>''')
    
    cols_joined = "\n".join(cols_xml)
    metadata_joined = "\n".join(metadata_xml)

    xml = f'''<?xml version=\'1.0\' encoding=\'utf-8\' ?>
<workbook original-version=\'18.1\' source-build=\'2026.3.0\' version=\'18.1\' xml:base=\'http://localhost\' xmlns:user=\'http://www.tableausoftware.com/xml/user\'>
  <document-format-change-manifest>
    <AccessibleZoneTabOrder />
    <IntuitiveSorting />
    <MapboxVectorStylesAndLayers />
    <MarkAnimation />
    <ObjectModelEncapsulateLegacy />
    <ObjectModelTableType />
    <SchemaViewerObjectModel />
    <SheetIdentifierTracking />
    <WindowsPersistSimpleIdentifiers />
  </document-format-change-manifest>
  <preferences>
    <preference name=\'ui.encoding.shelf.height\' value=\'24\' />
    <preference name=\'ui.shelf.height\' value=\'26\' />
  </preferences>
  <datasources>
    <datasource caption=\'ev_market_clean\' inline=\'true\' name=\'federated.ev_market_clean\' version=\'18.1\'>
      <connection class=\'federated\'>
        <named-connections>
          <named-connection caption=\'ev_market_clean\' name=\'textscan.ev_market_clean\'>
            <connection class=\'textscan\' directory=\'{csv_rel_dir}\' filename=\'{csv_filename}\' extract-engine=\'false\' server=\'\' />
          </named-connection>
        </named-connections>
        <relation connection=\'textscan.ev_market_clean\' name=\'ev_market_clean.csv\' table=\'[ev_market_clean#csv]\' type=\'table\'>
          <columns character-set=\'UTF-8\'>
{cols_joined}
          </columns>
        </relation>
        <metadata-records>
{metadata_joined}
        </metadata-records>
      </connection>
      <aliases enabled=\'yes\' />
      <!-- Calculated fields per TABLEAU_BUILD_GUIDE.md -->
      <column caption=\'Sales (K)\' datatype=\'real\' name=\'[Calculation_Sales_K]\' role=\'measure\' type=\'quantitative\'>
        <calculation class=\'tableau\' formula=\'SUM([annual_sales_units]) / 1000\' />
      </column>
      <column caption=\'Price per KM of Range\' datatype=\'real\' name=\'[Calculation_Price_Per_KM]\' role=\'measure\' type=\'quantitative\'>
        <calculation class=\'tableau\' formula=\'IF [range_km] &gt; 0 THEN [price_usd] / [range_km] END\' />
      </column>
      <column caption=\'Battery Capacity per 100 KM\' datatype=\'real\' name=\'[Calculation_Battery_Per_100KM]\' role=\'measure\' type=\'quantitative\'>
        <calculation class=\'tableau\' formula=\'IF [range_km] &gt; 0 THEN [battery_capacity_kwh] / [range_km] * 100 END\' />
      </column>
      <column caption=\'High Customer Rating\' datatype=\'string\' name=\'[Calculation_High_Rating]\' role=\'dimension\' type=\'nominal\'>
        <calculation class=\'tableau\' formula=\'IF [customer_rating] &gt;= 4 THEN &quot;4+ Stars&quot; ELSE &quot;Below 4 Stars&quot; END\' />
      </column>
      <column caption=\'Model Age\' datatype=\'integer\' name=\'[Calculation_Model_Age]\' role=\'measure\' type=\'quantitative\'>
        <calculation class=\'tableau\' formula=\'2026 - [model_year]\' />
      </column>
    </datasource>
  </datasources>
  <worksheets>
    <worksheet name=\'Sales by Region\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'string\' name=\'[market_region]\' role=\'dimension\' type=\'nominal\' />
            <column datatype=\'real\' name=\'[annual_sales_units]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[annual_sales_units]\' derivation=\'Sum\' name=\'[sum:annual_sales_units:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[market_region]\' derivation=\'None\' name=\'[none:market_region:nk]\' pivot=\'key\' type=\'nominal\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Bar\' />
            <encodings>
              <text column=\'[federated.ev_market_clean].[sum:annual_sales_units:qk]\' />
            </encodings>
            <style>
              <style-rule element=\'mark\'>
                <format attr=\'mark-labels-show\' value=\'true\' />
              </style-rule>
            </style>
          </pane>
        </panes>
        <rows>[federated.ev_market_clean].[none:market_region:nk]</rows>
        <cols>[federated.ev_market_clean].[sum:annual_sales_units:qk]</cols>
      </table>
    </worksheet>
    <worksheet name=\'Sales by Model Year\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'integer\' name=\'[model_year]\' role=\'dimension\' type=\'quantitative\' />
            <column datatype=\'real\' name=\'[annual_sales_units]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[annual_sales_units]\' derivation=\'Sum\' name=\'[sum:annual_sales_units:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[model_year]\' derivation=\'None\' name=\'[none:model_year:qk]\' pivot=\'key\' type=\'quantitative\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Line\' />
          </pane>
        </panes>
        <rows>[federated.ev_market_clean].[sum:annual_sales_units:qk]</rows>
        <cols>[federated.ev_market_clean].[none:model_year:qk]</cols>
      </table>
    </worksheet>
    <worksheet name=\'Category Performance\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'string\' name=\'[category]\' role=\'dimension\' type=\'nominal\' />
            <column datatype=\'real\' name=\'[annual_sales_units]\' role=\'measure\' type=\'quantitative\' />
            <column datatype=\'real\' name=\'[customer_rating]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[annual_sales_units]\' derivation=\'Sum\' name=\'[sum:annual_sales_units:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[customer_rating]\' derivation=\'Avg\' name=\'[avg:customer_rating:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[category]\' derivation=\'None\' name=\'[none:category:nk]\' pivot=\'key\' type=\'nominal\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Bar\' />
            <encodings>
              <tooltip column=\'[federated.ev_market_clean].[avg:customer_rating:qk]\' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.ev_market_clean].[none:category:nk]</rows>
        <cols>[federated.ev_market_clean].[sum:annual_sales_units:qk]</cols>
      </table>
    </worksheet>
    <worksheet name=\'Battery Technology\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'string\' name=\'[battery_type]\' role=\'dimension\' type=\'nominal\' />
            <column datatype=\'real\' name=\'[range_km]\' role=\'measure\' type=\'quantitative\' />
            <column datatype=\'real\' name=\'[annual_sales_units]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[range_km]\' derivation=\'Avg\' name=\'[avg:range_km:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[annual_sales_units]\' derivation=\'Sum\' name=\'[sum:annual_sales_units:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[battery_type]\' derivation=\'None\' name=\'[none:battery_type:nk]\' pivot=\'key\' type=\'nominal\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Bar\' />
            <encodings>
              <tooltip column=\'[federated.ev_market_clean].[sum:annual_sales_units:qk]\' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.ev_market_clean].[avg:range_km:qk]</rows>
        <cols>[federated.ev_market_clean].[none:battery_type:nk]</cols>
      </table>
    </worksheet>
    <worksheet name=\'Manufacturer Leaders\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'string\' name=\'[manufacturer]\' role=\'dimension\' type=\'nominal\' />
            <column datatype=\'real\' name=\'[annual_sales_units]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[annual_sales_units]\' derivation=\'Sum\' name=\'[sum:annual_sales_units:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[manufacturer]\' derivation=\'None\' name=\'[none:manufacturer:nk]\' pivot=\'key\' type=\'nominal\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Bar\' />
          </pane>
        </panes>
        <rows>[federated.ev_market_clean].[none:manufacturer:nk]</rows>
        <cols>[federated.ev_market_clean].[sum:annual_sales_units:qk]</cols>
      </table>
    </worksheet>
    <worksheet name=\'Price vs Range\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'string\' name=\'[category]\' role=\'dimension\' type=\'nominal\' />
            <column datatype=\'real\' name=\'[price_usd]\' role=\'measure\' type=\'quantitative\' />
            <column datatype=\'real\' name=\'[range_km]\' role=\'measure\' type=\'quantitative\' />
            <column datatype=\'real\' name=\'[customer_rating]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[price_usd]\' derivation=\'Avg\' name=\'[avg:price_usd:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[range_km]\' derivation=\'Avg\' name=\'[avg:range_km:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[customer_rating]\' derivation=\'Avg\' name=\'[avg:customer_rating:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[category]\' derivation=\'None\' name=\'[none:category:nk]\' pivot=\'key\' type=\'nominal\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Circle\' />
            <encodings>
              <lod column=\'[federated.ev_market_clean].[none:category:nk]\' />
              <tooltip column=\'[federated.ev_market_clean].[avg:customer_rating:qk]\' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.ev_market_clean].[avg:range_km:qk]</rows>
        <cols>[federated.ev_market_clean].[avg:price_usd:qk]</cols>
      </table>
    </worksheet>
    <worksheet name=\'Customer Ratings\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'string\' name=\'[category]\' role=\'dimension\' type=\'nominal\' />
            <column datatype=\'real\' name=\'[customer_rating]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[customer_rating]\' derivation=\'Avg\' name=\'[avg:customer_rating:qk]\' pivot=\'key\' type=\'quantitative\' />
            <column-instance column=\'[category]\' derivation=\'None\' name=\'[none:category:nk]\' pivot=\'key\' type=\'nominal\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Bar\' />
          </pane>
        </panes>
        <rows>[federated.ev_market_clean].[none:category:nk]</rows>
        <cols>[federated.ev_market_clean].[avg:customer_rating:qk]</cols>
      </table>
    </worksheet>
    <worksheet name=\'KPI Total Sales\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'real\' name=\'[annual_sales_units]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[annual_sales_units]\' derivation=\'Sum\' name=\'[sum:annual_sales_units:qk]\' pivot=\'key\' type=\'quantitative\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Text\' />
            <encodings>
              <text column=\'[federated.ev_market_clean].[sum:annual_sales_units:qk]\' />
            </encodings>
          </pane>
        </panes>
        <rows />
        <cols />
      </table>
    </worksheet>
    <worksheet name=\'KPI Avg Range\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'real\' name=\'[range_km]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[range_km]\' derivation=\'Avg\' name=\'[avg:range_km:qk]\' pivot=\'key\' type=\'quantitative\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Text\' />
            <encodings>
              <text column=\'[federated.ev_market_clean].[avg:range_km:qk]\' />
            </encodings>
          </pane>
        </panes>
        <rows />
        <cols />
      </table>
    </worksheet>
    <worksheet name=\'KPI Avg Price\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'real\' name=\'[price_usd]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[price_usd]\' derivation=\'Avg\' name=\'[avg:price_usd:qk]\' pivot=\'key\' type=\'quantitative\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Text\' />
            <encodings>
              <text column=\'[federated.ev_market_clean].[avg:price_usd:qk]\' />
            </encodings>
          </pane>
        </panes>
        <rows />
        <cols />
      </table>
    </worksheet>
    <worksheet name=\'KPI Avg Rating\'>
      <table>
        <view>
          <datasources>
            <datasource caption=\'ev_market_clean\' name=\'federated.ev_market_clean\' />
          </datasources>
          <datasource-dependencies datasource=\'federated.ev_market_clean\'>
            <column datatype=\'real\' name=\'[customer_rating]\' role=\'measure\' type=\'quantitative\' />
            <column-instance column=\'[customer_rating]\' derivation=\'Avg\' name=\'[avg:customer_rating:qk]\' pivot=\'key\' type=\'quantitative\' />
          </datasource-dependencies>
          <aggregation value=\'true\' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option=\'selection-relaxation-allow\'>
            <view>
              <breakdown value=\'auto\' />
            </view>
            <mark class=\'Text\' />
            <encodings>
              <text column=\'[federated.ev_market_clean].[avg:customer_rating:qk]\' />
            </encodings>
          </pane>
        </panes>
        <rows />
        <cols />
      </table>
    </worksheet>
  </worksheets>

  <!-- Dashboards -->
  <dashboards>
    <dashboard name=\'EV Market Intelligence Dashboard\'>
      <style />
      <size maxheight=\'900\' maxwidth=\'1300\' minheight=\'900\' minwidth=\'1300\' type=\'fixed\' />
      <zones>
        <zone h=\'100000\' id=\'1\' type-v2=\'layout-basic\' w=\'100000\' x=\'0\' y=\'0\'>
          <zone h=\'8000\' id=\'2\' name=\'title\' type-v2=\'title\' w=\'100000\' x=\'0\' y=\'0\'>
            <formatted-text>
              <run fontalignment=\'1\' fontcolor=\'#1b365d\' fontname=\'Segoe UI\' fontsize=\'18\' bold=\'true\'>EV Market Intelligence | Synthetic Dataset Analysis</run>
            </formatted-text>
          </zone>
          <!-- KPI Zone -->
          <zone h=\'12000\' id=\'3\' type-v2=\'layout-flow\' w=\'100000\' x=\'0\' y=\'8000\'>
            <zone h=\'12000\' id=\'4\' name=\'KPI Total Sales\' w=\'25000\' x=\'0\' y=\'8000\' />
            <zone h=\'12000\' id=\'5\' name=\'KPI Avg Range\' w=\'25000\' x=\'25000\' y=\'8000\' />
            <zone h=\'12000\' id=\'6\' name=\'KPI Avg Price\' w=\'25000\' x=\'50000\' y=\'8000\' />
            <zone h=\'12000\' id=\'7\' name=\'KPI Avg Rating\' w=\'25000\' x=\'75000\' y=\'8000\' />
          </zone>
          <!-- Middle Visuals Row -->
          <zone h=\'40000\' id=\'8\' type-v2=\'layout-flow\' w=\'100000\' x=\'0\' y=\'20000\'>
            <zone h=\'40000\' id=\'9\' name=\'Sales by Region\' w=\'50000\' x=\'0\' y=\'20000\' />
            <zone h=\'40000\' id=\'10\' name=\'Category Performance\' w=\'50000\' x=\'50000\' y=\'20000\' />
          </zone>
          <!-- Bottom Visuals Row -->
          <zone h=\'40000\' id=\'11\' type-v2=\'layout-flow\' w=\'100000\' x=\'0\' y=\'60000\'>
            <zone h=\'40000\' id=\'12\' name=\'Battery Technology\' w=\'33333\' x=\'0\' y=\'60000\' />
            <zone h=\'40000\' id=\'13\' name=\'Manufacturer Leaders\' w=\'33333\' x=\'33333\' y=\'60000\' />
            <zone h=\'40000\' id=\'14\' name=\'Price vs Range\' w=\'33334\' x=\'66666\' y=\'60000\' />
          </zone>
        </zone>
      </zones>
    </dashboard>
  </dashboards>

  <!-- Story (3 Scenes) -->
  <stories>
    <story name=\'EV Market Story\'>
      <style />
      <size maxheight=\'850\' maxwidth=\'1250\' minheight=\'850\' minwidth=\'1250\' type=\'fixed\' />
      <story-points>
        <story-point caption=\'Where is recorded demand concentrated?\' id=\'1\'>
          <description>Demand distribution across global geographic regions and major vehicle categories shows strong volume in South Asia and Latin America, driven largely by two-wheelers and hatchbacks.</description>
          <sheet name=\'Sales by Region\' />
        </story-point>
        <story-point caption=\'Which technology characteristics stand out?\' id=\'2\'>
          <description>Analysis of battery chemistry performance and pricing relative to range shows Solid-State and NMC chemistries leading range, with consistent degradation advantages in LFP packs.</description>
          <sheet name=\'Battery Technology\' />
        </story-point>
        <story-point caption=\'What should decision-makers compare next?\' id=\'3\'>
          <description>Examining top manufacturer volume alongside customer satisfaction ratings provides actionable segmentation benchmarks across fictional cohort models.</description>
          <sheet name=\'Manufacturer Leaders\' />
        </story-point>
      </story-points>
    </story>
  </stories>

  <windows>
    <window class=\'worksheet\' name=\'Sales by Region\'>
      <cards>
        <edge name=\'left\'>
          <strip size=\'160\'>
            <card type=\'pages\' />
            <card type=\'filters\' />
            <card type=\'marks\' />
          </strip>
        </edge>
        <edge name=\'top\'>
          <strip size=\'31\'>
            <card type=\'columns\' />
          </strip>
          <strip size=\'31\'>
            <card type=\'rows\' />
          </strip>
          <strip size=\'31\'>
            <card type=\'title\' />
          </strip>
        </edge>
      </cards>
    </window>
    <window class=\'dashboard\' maximized=\'true\' name=\'EV Market Intelligence Dashboard\'>
      <viewpoints />
      <active id=\'1\' />
    </window>
    <window class=\'story\' maximized=\'true\' name=\'EV Market Story\'>
      <viewpoints />
      <active id=\'1\' />
    </window>
  </windows>
</workbook>
'''
    return xml

def generate_workbooks():
    print("Building EV_Market_Intelligence.twb...")
    twb_content = build_twb_xml(csv_rel_dir="../data", csv_filename="ev_market_clean.csv")
    with open(TWB_PATH, 'w', encoding='utf-8') as f:
        f.write(twb_content)
    print(f"Wrote {TWB_PATH} ({os.path.getsize(TWB_PATH):,} bytes)")

    # Validate XML parsing
    tree = ET.parse(TWB_PATH)
    root = tree.getroot()
    print("XML syntax verification: VALID (Root tag:", root.tag, ")")

    # Validate with tableaudocumentapi
    wb = Workbook(str(TWB_PATH))
    print(f"tableaudocumentapi verification:")
    print(f"  - Worksheets found ({len(wb.worksheets)}): {wb.worksheets}")
    print(f"  - Dashboards found ({len(wb.dashboards)}): {wb.dashboards}")
    print(f"  - Datasources found ({len(wb.datasources)}): {[d.caption for d in wb.datasources]}")
    for ds in wb.datasources:
        print(f"    Fields count in '{ds.caption}': {len(ds.fields)}")
        calc_fields = [f.name for f in ds.fields.values() if f.calculation is not None]
        print(f"    Calculated fields: {calc_fields}")

    # Build packaged .twbx workbook
    print("\nBuilding packaged Tableau workbook EV_Market_Intelligence.twbx...")
    twbx_twb_content = build_twb_xml(csv_rel_dir="Data", csv_filename="ev_market_clean.csv")
    temp_twb_packaged = WORKSPACE / "tableau" / "_temp_packaged.twb"
    with open(temp_twb_packaged, 'w', encoding='utf-8') as f:
        f.write(twbx_twb_content)

    with zipfile.ZipFile(TWBX_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        # Put twb at root of archive
        zf.write(temp_twb_packaged, arcname="EV_Market_Intelligence.twb")
        # Put data inside Data/ folder
        zf.write(CSV_PATH, arcname="Data/ev_market_clean.csv")
    
    if temp_twb_packaged.exists():
        temp_twb_packaged.unlink()
    
    print(f"Wrote {TWBX_PATH} ({os.path.getsize(TWBX_PATH):,} bytes)")

    # Validate .twbx with tableaudocumentapi
    wb_pkg = Workbook(str(TWBX_PATH))
    print(f"tableaudocumentapi .twbx verification:")
    print(f"  - Worksheets found: {wb_pkg.worksheets}")
    print(f"  - Dashboards found: {wb_pkg.dashboards}")
    print(f"  - Datasources found: {[d.caption for d in wb_pkg.datasources]}")

if __name__ == '__main__':
    generate_workbooks()
