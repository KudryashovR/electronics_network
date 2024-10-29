from rest_framework import serializers

from network.models import NetworkNode, Product


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NetworkNode.

    Этот сериализатор используется для преобразования данных модели NetworkNode в формат JSON и обратно. Он исключает
    поле 'debt' из результата.
    """

    class Meta:
        """
        Метакласс, определяющий параметры сериализатора.

        Указывает модель, которую следует использовать, и список исключаемых полей.
        """

        model = NetworkNode
        exclude = ['debt']


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Этот сериализатор используется для преобразования данных модели Product в формат JSON и обратно. Он включает
    все поля модели.
    """

    class Meta:
        """
        Метакласс, определяющий параметры сериализатора.

        Указывает модель, которую следует использовать, и список включаемых полей ('__all__' означает все поля).
        """

        model = Product
        fields = '__all__'
