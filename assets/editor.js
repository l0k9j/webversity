let data_url = 'https://raw.githubusercontent.com/l0k9j/webversity/master/infra.json';

let colls = window.colls || {};
let Vue = window.Vue

Vue.component('data-item', {
  props: ['item'],
  data: function () {
    return {
      x: null
    }
  },
  methods: {
    item_type: function () {
      return this.subitem_type(this.item)
    },
    subitem_type: function (subitem) {
      let ret = 'literal';
      if (Array.isArray(subitem)) {
        ret = 'array'
      } else {
        if (subitem === null) {
          ret = 'null'
        } else {
          if (typeof subitem === 'object') {
            ret = 'dict'
          }
        }
      }
      return ret
    }
  },
  template: `
    <div>
      <ol v-if="item_type() == 'array'">
        <li v-for="subitem in item"><data-item :item="subitem"></data-item></li>
      </ol>
      <template v-if="item_type() == 'literal'">
        <input type="text" v-model="item">
      </template>
      <ul v-if="item_type() == 'dict'">
        <li v-for="(subitem, name) in item" :class="'type-'+subitem_type(subitem)">{{name}}: <data-item :item="subitem"></data-item></li>
      </ul>
    </div>
  `
})


var app = new Vue({
  el: '#editor',
  data: {
    colls: colls,
    selection: {
      coll: null
    }
  },
  mounted: function () {
    let self = this
    if (!this.colls && data_url) {
      fetch(data_url)
        .then(response => response.json())
        .then(function (data) {
          Vue.set(self, 'colls', data)
          self.init_selection()
        }
        )
    }
    self.init_selection()
  },
  methods: {
    init_selection: function () {
      if (this.colls) {
        this.select_coll(Object.values(this.colls)[1])
      }
    },
    select_coll: function (coll) {
      this.selection.coll = coll
    }
  }
})
