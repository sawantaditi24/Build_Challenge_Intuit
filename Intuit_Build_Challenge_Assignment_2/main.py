"""
Main application for data analysis on CSV sales data.
Demonstrates functional programming with Stream operations, aggregations, and lambda expressions.
"""

import sys
from pathlib import Path
from src.csv_reader import CSVReader
from src.data_analyzer import DataAnalyzer


def format_currency(amount: float) -> str:
    """
    Format amount as currency string.

    Args:
        amount: Numeric amount to format

    Returns:
        Formatted currency string
    """
    return f"${amount:,.2f}"


def print_section_header(title: str):
    """
    Print a formatted section header.

    Args:
        title: Section title to display
    """
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_dictionary(title: str, data: dict, value_formatter=None):
    """
    Print a dictionary in formatted manner.

    Args:
        title: Title for the dictionary output
        data: Dictionary to print
        value_formatter: Optional function to format values
    """
    print(f"\n{title}:")
    print("-" * 80)
    for key, value in sorted(data.items()):
        if value_formatter:
            value = value_formatter(value)
        print(f"  {key:30s}: {value:>15s}")


def print_list(title: str, data: list, item_formatter=None):
    """
    Print a list in formatted manner.

    Args:
        title: Title for the list output
        data: List to print
        item_formatter: Optional function to format each item
    """
    print(f"\n{title}:")
    print("-" * 80)
    for i, item in enumerate(data, 1):
        if item_formatter:
            item = item_formatter(item)
        print(f"  {i}. {item}")


def main():
    """
    Main function that performs all data analyses and prints results to console.
    """
    # Get CSV file path
    script_dir = Path(__file__).parent
    csv_file = script_dir / "data" / "sales_data.csv"
    
    if not csv_file.exists():
        print(f"Error: CSV file not found at {csv_file}")
        sys.exit(1)
    
    print_section_header("Intuit Sales Data Analysis")
    print(f"\nAnalyzing data from: {csv_file}")
    print(f"Using functional programming: Streams, Lambdas, and Aggregations")
    
    try:
        # Initialize CSV reader and data analyzer
        csv_reader = CSVReader(str(csv_file))
        analyzer = DataAnalyzer(csv_reader)
        
        # Analysis 1: Total Revenue
        print_section_header("Analysis 1: Total Revenue")
        total_revenue = analyzer.get_total_revenue()
        print(f"\nTotal Revenue: {format_currency(total_revenue)}")
        
        # Analysis 2: Revenue by Category
        print_section_header("Analysis 2: Revenue by Product Category")
        revenue_by_category = analyzer.get_revenue_by_category()
        print_dictionary("Revenue by Category", revenue_by_category, format_currency)
        
        # Analysis 3: Revenue by Region
        print_section_header("Analysis 3: Revenue by Region")
        revenue_by_region = analyzer.get_revenue_by_region()
        print_dictionary("Revenue by Region", revenue_by_region, format_currency)
        
        # Analysis 4: Revenue by Customer Type
        print_section_header("Analysis 4: Revenue by Customer Type")
        revenue_by_customer = analyzer.get_revenue_by_customer_type()
        print_dictionary("Revenue by Customer Type", revenue_by_customer, format_currency)
        
        # Analysis 5: Top Products by Revenue
        print_section_header("Analysis 5: Top 5 Products by Revenue")
        top_products = analyzer.get_top_products_by_revenue(top_n=5)
        print("\nTop Products:")
        print("-" * 80)
        for i, product in enumerate(top_products, 1):
            print(f"  {i}. {product['Product']:40s}: {format_currency(product['Total_Revenue']):>15s}")
        
        # Analysis 6: Average Revenue per Transaction
        print_section_header("Analysis 6: Average Revenue per Transaction")
        avg_revenue = analyzer.get_average_revenue_per_transaction()
        print(f"\nAverage Revenue per Transaction: {format_currency(avg_revenue)}")
        
        # Analysis 7: Sales by Month
        print_section_header("Analysis 7: Sales by Month")
        sales_by_month = analyzer.get_sales_by_month()
        print_dictionary("Monthly Sales", sales_by_month, format_currency)
        
        # Analysis 8: Products by Category
        print_section_header("Analysis 8: Products Grouped by Category")
        products_by_category = analyzer.get_products_by_category()
        print("\nProducts by Category:")
        print("-" * 80)
        for category, products in sorted(products_by_category.items()):
            print(f"\n  {category}:")
            for product in products:
                print(f"    - {product}")
        
        # Analysis 9: High Value Transactions
        print_section_header("Analysis 9: High Value Transactions (>= $100,000)")
        high_value = analyzer.get_high_value_transactions(threshold=100000.0)
        print(f"\nNumber of High Value Transactions: {len(high_value)}")
        if high_value:
            print("\nHigh Value Transactions:")
            print("-" * 80)
            for i, transaction in enumerate(high_value[:10], 1):  # Show first 10
                date = transaction.get('Date', 'N/A')
                product = transaction.get('Product', 'N/A')
                revenue = format_currency(float(transaction.get('Total_Revenue', '0')))
                print(f"  {i}. {date} | {product:30s} | {revenue:>15s}")
            if len(high_value) > 10:
                print(f"  ... and {len(high_value) - 10} more transactions")
        
        # Analysis 10: Revenue by Product and Region (Nested Grouping)
        print_section_header("Analysis 10: Revenue by Product and Region (Nested Grouping)")
        product_region_revenue = analyzer.get_revenue_by_product_and_region()
        print("\nRevenue by Product and Region:")
        print("-" * 80)
        for product in sorted(product_region_revenue.keys()):
            print(f"\n  {product}:")
            regions = product_region_revenue[product]
            for region in sorted(regions.keys()):
                revenue = format_currency(regions[region])
                print(f"    {region:20s}: {revenue:>15s}")
        
        # Analysis 11: Total Quantity Sold
        print_section_header("Analysis 11: Total Quantity Sold")
        total_quantity = analyzer.get_total_quantity_sold()
        print(f"\nTotal Quantity Sold: {total_quantity:,} units")
        
        # Analysis 12: Average Quantity per Transaction
        print_section_header("Analysis 12: Average Quantity per Transaction")
        avg_quantity = analyzer.get_average_quantity_per_transaction()
        print(f"\nAverage Quantity per Transaction: {avg_quantity:,.2f} units")
        
        # Summary
        print_section_header("Analysis Summary")
        print("\nAll analyses completed successfully!")
        print(f"Total Records Analyzed: {len(csv_reader.read_all_records())}")
        print(f"Total Revenue: {format_currency(total_revenue)}")
        print(f"Total Quantity: {total_quantity:,} units")
        print(f"Average Revenue per Transaction: {format_currency(avg_revenue)}")
        print(f"Number of Categories: {len(revenue_by_category)}")
        print(f"Number of Regions: {len(revenue_by_region)}")
        print(f"Number of Customer Types: {len(revenue_by_customer)}")
        
        print_section_header("Analysis Complete")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

