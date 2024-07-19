# this script will contain utility functions that will be used in the main script


def format_eleveur_for_selectbox(eleveur: dict) -> str:
    """
    Format the eleveur dictionary for the selectbox.

    Args:
        eleveur (dict): Eleveur data

    Returns:
        str: Formatted eleveur data
    """
    return f"{eleveur['email']} ({eleveur['nom']} from {eleveur['societe']})"
