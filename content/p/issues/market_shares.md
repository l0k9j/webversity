csv_markets=markets.csv

{% for market in markets.market.unique() %}
## {{market|title}}

{% with products = markets[markets['market']==market] %}
<table class="table is-striped is-narrow">
<thead>
<tr>
<th>Share (%)</th>
<th>Product</th>
<th>Producer</th>
</tr>
</thead>
<tbody>
{% for i, r in products.iterrows() %}
<tr>
<td>{{ r.share|int }}</td>
<td>{{ r['product'] }}</td>
<td>{{ r.producer }}</td>
</tr>
{% endfor %}
<tr>
<td>{{ (100-products['share'].sum())|int }}</td>
<td>All others</td>
<td></td>
</tr>
</tbody>
</table>
{% endwith %}
{% endfor %}

