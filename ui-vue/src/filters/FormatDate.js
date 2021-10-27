import Vue from 'vue'
import moment from 'moment';

Vue.filter('formatDate', function(value, format = 'MM/DD/YYYY hh:mm') {
    if (value) {
        return moment(String(value)).format(format)
    }
});