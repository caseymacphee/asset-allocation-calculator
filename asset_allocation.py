from decimal import Decimal


class Vertice(object):
    def __init__(self, label, percentage, allocation_type='PERCENT', description=None, sub_nodes=set()):
        self.label = label
        self.percentage = percentage
        self.amount = None
        self.description = description
        self.sub_nodes = sub_nodes
        if allocation_type not in (
            'PERCENTAGE', 'EVEN', 'REMAINDER'):
            raise ValueError(
                "Cannot determine distribution amount of the type: {}".format(
                    allocation_type))
        if percentage is not None and allocation_type != 'PERCENTAGE':
            raise ValueError(
                "Cannot use percentage based allocation with none PERCENTAGE allocation type")
        if percentage is None and allocation_type == 'PERCENTAGE':
            raise ValueError(
                "Percentage allocation types must define a percentage.")
        self.allocation_type = allocation_type
 

class AssetCategory(Vertice):
    def __init__(self, label, percentage, allocation_type='PERCENTAGE', description=None, amount=None):
        super(AssetCategory, self).__init__(
            label,
            percentage,
            allocation_type=allocation_type,
            description=description)
        self.amount = amount


class Asset(Vertice):
    def __init__(
        self,
        label,
        allocation_type='PERCENTAGE',
        percentage=None,
        description=None, 
        ticker=None, 
        num_units=None,
        price=None):
        super(Asset, self).__init__(
            label,
            percentage,
            allocation_type=allocation_type,
            description=description)
        self.amount = None
        self.ticker = ticker
        self.num_units = num_units
        self.price = price


def sort_vertice(obj):
    return obj.percentage

class AllocationTree(object):
    def __init__(self, root_node):
        self.root_node = root_node

    def calculate_amounts(self, current_node=None, last_amount=None, last_percentage=None, depth=0):
        if not current_node:
            current_node = self.root_node
        if not last_amount:
            last_amount = self.root_node.amount
        if not last_percentage:
            last_percentage = self.root_node.percentage
        indent = "    " * depth
        print(
            indent + 
            "-{}".format(
                current_node.label))
        print(
            indent + "    " +
            "Allocation method: {}".format(current_node.allocation_type.title()))
        print(
            indent + 
            "    " + 
            "Percentage of root category: {}%".format(
                current_node.percentage * 100))
        allocated_amount = last_amount * current_node.percentage
        allocated_percentage = last_percentage * current_node.percentage
        print(
            indent + 
            "    "  + 
            "Total allocation percentage: {}%".format(
                allocated_percentage * 100))
        print(
            indent + 
            "    "  + 
            "Total allocaton amount: ${}".format(
                allocated_amount))
        print("")
        if current_node.sub_nodes:
            total_percent = 0
            remainders = [i for i in current_node.sub_nodes if i.allocation_type == 'REMAINDER']
            percentages = [i for i in current_node.sub_nodes if i.allocation_type == 'PERCENTAGE']
            percentages.sort(key=sort_vertice, reverse=True)
            even_dist = {i for i in current_node.sub_nodes if i.allocation_type == 'EVEN'}
            if len(even_dist) > 0 and (len(percentages) > 0 or len(remainders) > 0):
                raise ValueError("Cannot mix even distribution and remainder/percentages in a category.")
            for node in percentages:
                total_percent += node.percentage
                self.calculate_amounts(
                    current_node=node,
                    last_amount=allocated_amount,
                    last_percentage=allocated_percentage,
                    depth=depth+1)
            percent_diff = Decimal('1.0') - total_percent
            if remainders:
                percent_per_remainder = percent_diff / len(remainders)
                for node in remainders:
                    node.percentage = percent_per_remainder
                    self.calculate_amounts(
                        current_node=node,
                        last_amount=allocated_amount,
                        last_percentage=allocated_percentage,
                        depth=depth+1)
                percent_diff = Decimal('0.0')
            if even_dist:
                percent_per_even_dist =  Decimal('1.0') / len(even_dist)
                for node in even_dist:
                    node.percentage = percent_per_even_dist
                    self.calculate_amounts(
                        current_node=node,
                        last_amount=allocated_amount,
                        last_percentage=allocated_percentage,
                        depth=depth+1)
                percent_diff = Decimal('0.0')
            if percent_diff > Decimal('0.0'):
                self.calculate_amounts(
                    current_node=AssetCategory(
                        "Unallocated",
                        percent_diff),
                        last_amount=allocated_amount,
                        last_percentage=allocated_percentage,
                        depth=depth+1)
            if percent_diff < Decimal('0.0'):
                raise ValueError("Asset allocation group exceeds %100 of root category: {} by {}%".format(
                    current_node.label,
                    percent_diff * -100))

