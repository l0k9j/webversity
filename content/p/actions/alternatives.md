csv_prods_js=products.csv
[Work in Progress]

{% for category in prods_js.category.unique() %}
## {{category}}
<table>
<tr>
<td>Name</td>
<td>Privacy</td>
<td>Open Source</td>
<td>First release</td>
</tr>
{% for i, r in prods_js[prods_js['category']==category].iterrows() %}
{% if r.dominant != 1 %}
<tr>
<td><a href="{{ r.link }}">{{ r.title }}</td>
<td class="score-{{r.privacy|int}}">{{r.privacy|int}}</td>
<td class="score-{{r.opensource|int}}">{{r.opensource|int}}</td>
<td>{{r.since}}</td>
</tr>
{% endif %} 
{% endfor %}
</tr>
{% endfor %}

