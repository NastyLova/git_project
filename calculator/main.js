var app = new Vue({
    el: '#app',
    data: {
        costall: '',
        percent: '',
        terms: 0,
        summ: 0,
        dailypercent: 0,
        expiration_date: new Date(),
        date: new Date()

    },
    methods:{
        calculate(){
            this.summ = this.percent * this.costall / 100 * this.terms
            this.dailypercent = this.percent * this.costall / 100
            this.expiration_date.setDate(this.expiration_date.getDate() + +this.terms)
        }
    }
  })
  