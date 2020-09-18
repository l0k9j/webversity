csv_markets=markets.csv

Unless otherwise stated the following numbers apply to the global market.
Click on a number for a link to its source. Note that given the scale
of the markets and variety of methods of measurement the accuracy is not
very high but the proportion of the distributions are generally reliable.

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
<td class="market-share"><div style="width:{{r.share|int}}%;">
<a href="{{r.source}}" target="_blank" title="See source">{{ r.share|int }}</a>
</div></td>
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

{% for i, r in products.iterrows() %}
{% if r.comment %}
<p>{{r.comment}}</p>
{% endif %}
{% endfor %}

{% endwith %}
{% endfor %}

## Sources

Our main sources for the above statistics:

* [StatCounter Global Stats](//gs.statcounter.com)
* [Net Marketshare](//netmarketshare.com)
* [W3Counter](//www.w3counter.com/globalstats.php)
* [Wikimedia Analytics](//analytics.wikimedia.org/dashboards/browsers/#all-sites-by-os)
