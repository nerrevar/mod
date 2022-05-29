from rest_framework import serializers
from .models import Image, Category

class ImagePostSerializer(serializers.Serializer):
    author = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects)
    cover = serializers.ImageField()


    def create(self, validated_data):
        return Image.objects.create(**validated_data)



class TaggedObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Image):
            serializer = ImageSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class ImageSerializer(serializers.ModelSerializer):
    author = serializers.CharField(max_length=40)
    title = serializers.CharField(max_length=40)
    description = serializers.CharField(max_length=150)
    cover = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    category = serializers.ReadOnlyField(source='category.name')
    user = serializers.EmailField()
    #ratings = TaggedObjectRelatedField(read_only=True)

    class Meta:
        model = Image
        fields = "__all__"


    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.cover.url)