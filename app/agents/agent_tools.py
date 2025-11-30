from agents import function_tool

@function_tool
def get_the_puzzle_solution():
    """this is the answer to the puzzle"""
    return list(range(1,16))