from rest_framework import serializers

from postings.models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer): #forms.modelForm
	url 		= serializers.SerializerMethodField(read_only=True)
	class Meta:
		model  = BlogPost
		fields =[
			'url',
			'pk',
			'user',
			'title',
			'content',
			'timestamp',
		]
		read_only_fields= ['id','user']
	#converts to json
	#validations for data passed

	def get_url(self,obj):
		request = self.context.get("request")
		return obj.get_api_url(request=request)

	def validate_title(self,value):
		qs = BlogPost.objects.filter(title__iexact=value)
		if self.instance:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise serializers.validationError("the title has already been used ")
		return value

