import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from datetime import datetime, timedelta

def advanced_visualization_demo():
    """Demo function showcasing advanced visualization capabilities"""
    
    st.title("📊 Advanced Data Visualization Demo")
    st.markdown("This demo showcases the visualization capabilities of the SQL Assistant")
    
    # Create sample data for demonstration
    @st.cache_data
    def load_demo_data():
        # Sales data over time
        dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
        sales_data = {
            'date': dates,
            'sales': [1000 + 200 * (i % 30) + 50 * ((i % 7) - 3) + 
                     100 * (1 if i % 7 < 5 else 0) for i in range(len(dates))],
            'region': ['North', 'South', 'East', 'West'][i % 4] for i in range(len(dates))
        }
        
        # Department performance
        dept_data = {
            'department': ['Engineering', 'Sales', 'Marketing', 'HR', 'Support'],
            'employees': [25, 15, 12, 8, 10],
            'avg_salary': [85000, 65000, 70000, 60000, 55000],
            'performance_score': [8.5, 9.2, 7.8, 8.0, 8.7]
        }
        
        # Product categories
        product_data = {
            'category': ['Software', 'Hardware', 'Services', 'Training', 'Support'],
            'revenue': [500000, 300000, 200000, 150000, 100000],
            'units_sold': [1000, 500, 800, 600, 1200]
        }
        
        return pd.DataFrame(sales_data), pd.DataFrame(dept_data), pd.DataFrame(product_data)
    
    sales_df, dept_df, product_df = load_demo_data()
    
    # Visualization options
    st.sidebar.header("Visualization Options")
    viz_type = st.sidebar.selectbox(
        "Choose visualization type:",
        ["Sales Trends", "Department Analysis", "Product Performance", "Combined Dashboard"]
    )
    
    if viz_type == "Sales Trends":
        st.subheader("📈 Sales Trends Over Time")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Line chart
            fig_line = px.line(
                sales_df, 
                x='date', 
                y='sales', 
                color='region',
                title="Daily Sales by Region"
            )
            st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            # Area chart
            fig_area = px.area(
                sales_df.groupby(['date', 'region'])['sales'].sum().reset_index(),
                x='date',
                y='sales',
                color='region',
                title="Cumulative Sales by Region"
            )
            st.plotly_chart(fig_area, use_container_width=True)
        
        # Heatmap
        sales_pivot = sales_df.set_index('date').groupby([
            sales_df['date'].dt.month, 
            sales_df['region']
        ])['sales'].mean().unstack()
        
        fig_heatmap = px.imshow(
            sales_pivot,
            title="Average Monthly Sales by Region",
            labels=dict(x="Region", y="Month", color="Sales"),
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    elif viz_type == "Department Analysis":
        st.subheader("🏢 Department Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart
            fig_bar = px.bar(
                dept_df,
                x='department',
                y='employees',
                color='avg_salary',
                title="Employee Count by Department",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Scatter plot
            fig_scatter = px.scatter(
                dept_df,
                x='employees',
                y='avg_salary',
                size='performance_score',
                color='department',
                title="Salary vs Employee Count",
                hover_data=['performance_score']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Radar chart
        fig_radar = go.Figure()
        
        categories = ['Employees', 'Avg Salary', 'Performance']
        
        for _, row in dept_df.iterrows():
            # Normalize values for radar chart
            values = [
                row['employees'] / dept_df['employees'].max() * 100,
                row['avg_salary'] / dept_df['avg_salary'].max() * 100,
                row['performance_score'] / dept_df['performance_score'].max() * 100
            ]
            values.append(values[0])  # Close the polygon
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=row['department']
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            title="Department Performance Radar Chart"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    elif viz_type == "Product Performance":
        st.subheader("📦 Product Category Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig_pie = px.pie(
                product_df,
                values='revenue',
                names='category',
                title="Revenue Distribution by Category"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Sunburst chart (hierarchical)
            fig_sunburst = px.sunburst(
                product_df,
                path=['category'],
                values='units_sold',
                title="Units Sold by Category"
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)
        
        # Dual axis chart
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_dual.add_trace(
            go.Bar(x=product_df['category'], y=product_df['revenue'], name="Revenue"),
            secondary_y=False,
        )
        
        fig_dual.add_trace(
            go.Scatter(x=product_df['category'], y=product_df['units_sold'], 
                      mode='lines+markers', name="Units Sold", line=dict(color='red')),
            secondary_y=True,
        )
        
        fig_dual.update_xaxes(title_text="Product Category")
        fig_dual.update_yaxes(title_text="Revenue ($)", secondary_y=False)
        fig_dual.update_yaxes(title_text="Units Sold", secondary_y=True)
        fig_dual.update_layout(title_text="Revenue vs Units Sold by Category")
        
        st.plotly_chart(fig_dual, use_container_width=True)
    
    elif viz_type == "Combined Dashboard":
        st.subheader("📊 Executive Dashboard")
        
        # KPI metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_sales = sales_df['sales'].sum()
            st.metric("Total Sales", f"${total_sales:,.0f}", "12.5%")
        
        with col2:
            total_employees = dept_df['employees'].sum()
            st.metric("Total Employees", total_employees, "3")
        
        with col3:
            avg_performance = dept_df['performance_score'].mean()
            st.metric("Avg Performance", f"{avg_performance:.1f}", "0.2")
        
        with col4:
            total_revenue = product_df['revenue'].sum()
            st.metric("Total Revenue", f"${total_revenue:,.0f}", "8.7%")
        
        # Combined visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales trend (simplified)
            monthly_sales = sales_df.groupby(sales_df['date'].dt.month)['sales'].sum()
            fig_trend = px.line(
                x=monthly_sales.index,
                y=monthly_sales.values,
                title="Monthly Sales Trend",
                labels={'x': 'Month', 'y': 'Sales'}
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            # Department budget allocation
            fig_budget = px.treemap(
                dept_df,
                path=['department'],
                values='employees',
                color='avg_salary',
                title="Department Resource Allocation"
            )
            st.plotly_chart(fig_budget, use_container_width=True)
        
        # Bottom section - detailed table
        st.subheader("📋 Detailed Data")
        
        tab1, tab2, tab3 = st.tabs(["Sales Data", "Department Data", "Product Data"])
        
        with tab1:
            st.dataframe(sales_df.head(20), use_container_width=True)
        
        with tab2:
            st.dataframe(dept_df, use_container_width=True)
        
        with tab3:
            st.dataframe(product_df, use_container_width=True)

if __name__ == "__main__":
    advanced_visualization_demo()
