{
    'name': 'My Library',
    'summary': 'Manage books easily',
    'author': 'Chike Chiagbaizu',
    'maintainer': 'Chike Chiagbaizu',
    'sequence': 1,
    'license': 'LGPL-3',
    'version': '19.0.1.0.0',
    'installable': True,
    'application': True,
    'category': 'Education',
    'depends': [
        'base',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_book_category_view.xml',
        'views/library_book_action.xml',
        'views/library_book_category_action.xml',
        'views/library_menus.xml',
    ],
}