#-----------------------------------------------------------------------------
# imports (at the top)
#-----------------------------------------------------------------------------
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly, render_widget
from shinyswatch import theme
from palmerpenguins import load_penguins
import palmerpenguins
import seaborn as sns
from shiny import reactive, render
from faicons import icon_svg
import json
from pathlib import Path
import pandas as pd

#-----------------------------------------------------------------------------
# define a reactive calc to filter the life expectancy seaborn dataset
#-----------------------------------------------------------------------------
lec_df: pd.DataFrame  = pd.read_csv(Path(__file__).parent / "example.csv")

#-----------------------------------------------------------------------------
# The overall page options
#-----------------------------------------------------------------------------
# Name the page
ui.page_opts(title="Sean's Life Expectancy Dashboard", fillable=True)

# Add a color theme to the dashboard
theme.vapor()


#-----------------------------------------------------------------------------
# A sidebar
#-----------------------------------------------------------------------------
with ui.sidebar(open="open"):  
    ui.HTML('<h3 style="font-size: medium;">Dashboard Configuration Options</h3>')
    with ui.accordion():
        with ui.accordion_panel("Country Filter"):
            ui.input_checkbox_group("selected_country_list", "Filter by Country:", 
                                choices=["Japan", "Germany", "France", "Great Britain", "USA", "Canada"], 
                                selected=["Japan"], inline=True)
        with ui.accordion_panel("Histogram Bins Configuration"):
            ui.input_numeric("plotly_bin_count", "# of Histogram Bins:", value=200, min=1, max=300)
        with ui.accordion_panel("Seaborn Bins Slider"):
            ui.input_slider("seaborn_bin_count", "# of Seaborn Bins:", min=1, max=300, value=200)

    

    ui.hr()
    ui.a("Project 6 - Custom Interactive App", href="https://github.com/SMStclair/cintel-06-custom", target="_blank")


#-----------------------------------------------------------------------------
# The main section with ui cards, value boxes, and space for grids and charts
#-----------------------------------------------------------------------------
with ui.accordion(id="acc", open="closed"):

    with ui.accordion_panel("Data Grid"):
        @render.data_frame
        def lec_datagrid():
            return render.DataGrid(lec_df)
                

# Navigation Card Tabset (Click on a tab to show contents) for up to 3 charts
with ui.navset_card_tab(id="tab"):
    

    with ui.nav_panel("Plotly Bar Chart"):

        @render_plotly
        def plot1():
            return px.histogram(dat(), y="Country")
    
    with ui.nav_panel("Plotly Scatterplot"):
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            plotly_scatter = px.scatter(
                dat(),
                x="Spending_USD",
                y="Life_Expectancy",
                color="Country",
                size_max=8,
                labels={
                    "Spending_USD": "Spending USD",
                    "Life_Expectancy": "Life Expectancy",
                },
            )
            return plotly_scatter
# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., lec_df()) will be updated when the data changes.

@reactive.calc
def dat():
    return lec_df[lec_df["Country"].isin(input.selected_country_list())]
