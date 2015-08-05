"""
Common utility methods useful for credit app.
"""

from xmodule.modulestore.django import modulestore
from xmodule.modulestore import ModuleStoreEnum


def is_in_course_tree(block):
    """ Check that the XBlock is in the course tree.

    It is possible that the XBlock is not in the course tree if its parent has
    been deleted and is now an orphan.

    Args:
        block (xblock): XBlock mixin

    Returns:
        bool: True or False
    """
    ancestor = block.get_parent()
    while ancestor is not None and ancestor.location.category != "course":
        ancestor = ancestor.get_parent()

    return ancestor is not None


def get_course_xblocks(course_key, category):
    """ Retrieve all XBlocks in the course for a particular category.

    Args:
        course_key (CourseKey): Identifier for the course.
        category (str): Category of XBlock.

    Returns:
        List of XBlocks that are published and haven't been deleted.

    """
    xblocks = [
        block for block in modulestore().get_items(
            course_key,
            qualifiers={"category": category},
            revision=ModuleStoreEnum.RevisionOption.published_only,
        )
        if is_in_course_tree(block)
    ]

    return xblocks