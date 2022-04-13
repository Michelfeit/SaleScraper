class Product:
    """
    This class represents a discounted product from a supermarket complete with its
    name,
    price,
    an image representation in form of an url,
    its discount,
    and whether it is a promotional price.
    """
    _name = ''
    _img_url = ''
    _promotional = False
    _price = 0
    _discount = 0  # between 0 and 1 -> discount by 25% means discount = 0.25
    _portion_size_info = ''
    _price_per_unit = ''

    def __init__(self, name: str, img_url: str, price: float, discount: float,
                 promotional: bool, portion_size_info: str, price_per_unit: str):
        """
        constructor for a product
        :param name: the name of the product
        :param img_url: the link to the image representation
        :param price: the price of the product
        :param discount: the percentage value of the discount
        :param promotional: whether the product is promoted
        :param portion_size_info: information about the sizing of the portions
        :param price_per_unit: the price per unit as string
        """
        self._name = name
        self._img_url = img_url
        self._price = price
        self._discount = discount
        self._promotional = promotional
        self._portion_size_info = portion_size_info
        self._price_per_unit = price_per_unit

    def str(self) -> str:
        """
        provides a string representation of a product
        :return: string containing all necessary info about the product
        """
        rep = self._name + ', ' + str(self._price)
        if self._promotional:
            rep += '(Aktionspreis)'
        else:
            rep += '(-' + str(int((self._discount * 100))) + '%)'
        rep += '\n' + 'url: ' + self._img_url
        return rep
