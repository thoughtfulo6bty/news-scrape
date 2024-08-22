import re


def count_phrases(title: str, **kwargs: str) -> int:
    """
    Counts the number of words in the title and optionally in the description.

    Args:
        title (str): The title of the text to count the words from.
        **kwargs (str): Optional keyword arguments, particularly 'description' to include additional words in the count.

    Returns:
        int: The total number of words in the title and, if provided, the description.
    """
    description = kwargs.get('description', None)
    title_len = len(title.split())
    if description:
        return title_len + len(description.split())
    else:
        return title_len


def contains_money(title: str, **kwargs: str) -> bool:
    # TODO: implements more patterns to check money in description and title or fuzzy search
    """
    Checks if the title (and optionally the description) contains a money-related pattern.

    The function searches for patterns representing monetary values, either with or without
    a currency symbol (like "$" or "USD"). The recognized patterns are as follows:
    
    - Dollar sign ($) followed by 1 to 3 digits, optionally followed by a comma or dot and another 
      set of 3 digits (as a thousand separator). This can be followed by an optional dot or comma 
      and 1 to 2 digits (as a decimal separator).
        Example: "$100", "$1,000", "$1,000.50"
    
    - 1 to 3 digits optionally followed by a comma or dot and another set of 3 digits (as a 
      thousand separator), followed by an optional dot or comma and 1 to 2 digits (as a decimal separator), 
      followed by a space and the currency ('dollars' or 'USD').
        Example: "100 dollars", "1,000 USD", "1,000.50 dollars", "$ 11,1", "$11,1", "$11", "$ 11"

    Args:
        title (str): The title of the text to check for monetary values.
        **kwargs (str): Optional keyword arguments, particularly 'description' to include 
                        additional text in the check.

    Returns:
        bool: True if a money-related pattern is found, False otherwise.
    """    
    description = kwargs.get('description', None)
    
    money_pattern = re.compile(
        r"""
        (                   # Start of a capturing group
            \$\s?           # Dollar sign ($), followed by an optional space
            \d{1,3}         # 1 to 3 digits
            (?:             # Start of a non-capturing group for thousand/decimal handling
                [.,]\d{3}   # A dot or comma followed by 3 digits (thousand separator)
            )*              # This group can occur zero or more times
            (?:             # Start of a non-capturing group for decimals
                [.,]\d{1,2} # A dot or comma followed by 1 to 2 digits (decimal)
            )?              # This group is optional (may or may not exist)
        )
        |                   # Or
        (\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?) # Number format without a dollar sign
        \s?                 # Optional space
        (dólares|USD)       # Currency specified as 'dollars' or 'USD'
        """,
        re.VERBOSE | re.IGNORECASE
    )

    if description:
        title = ' '.join([title, description]).strip()
    return bool(money_pattern.search(title))
