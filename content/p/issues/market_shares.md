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
<td class="market-share"><div style="width:{{r.share|int}}%;">{{ r.share|int }}</div></td>
<td>{{ r['product'] }}</td>
<td>{{ r.producer }}</td>
</tr>
{% endfor %}
{% with rest = 100-products['share'].sum() %}
<tr>
<td class="market-share"><div style="width:{{rest|int}}%;background-color:pink;">{{ rest|int }}</div></td>
<td>All others</td>
<td></td>
</tr>
{% endwith %}
</tbody>
</table>
{% endwith %}
{% endfor %}

