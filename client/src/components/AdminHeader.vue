<template>
  <div class="header" id="sol-header">
    <div class="logo">
      <img alt="Logo" width="250" v-bind:src="Logo" />
    </div>
    <div class="restOfHeader">
      <div class="table">
        <div class="row">
          <div class="title">
            <h1>{{ Name }}</h1>
          </div>
        </div>
      </div>
      <TabBar />
      <UIBar />
    </div>
    <div class="calendar">
      <v-date-picker
        v-model="selectedDate"
        :max-date="new Date()"
        :attributes="calendarAttributes"
        :is-required="true"
        is-inline
      ></v-date-picker>
    </div>
  </div>
</template>

<script>
import TabBar from "./TabBar.vue";
import UIBar from "./UIBar.vue";

export default {
  name: "Header",
  components: {
    TabBar,
    UIBar
  },
  data() {
    return {
      calendarAttributes: [
        {
          key: "today",
          highlight: "red",
          dates: new Date()
        }
      ]
    };
  },
  computed: {
    selectedDate: {
      get() {
        return this.$store.state.selectedDate;
      },
      set(value) {
        this.$store.commit("setSelectedDate", value);
        this.$store
          .dispatch("fetchEntriesByDate", value)
          .catch(function(reason) {
            alert(reason);
          });
      }
    },
    Name() {
      return this.$store.state.appName;
    },
    Logo() {
      return this.$store.state.logo;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
div.header {
  width: 100%;
  display: block;
  overflow: hidden;
  border-bottom: @mediumBorder;
}
div.logo {
  display: inline-block;
  margin-left: 1em;
  width: 250px;
  padding-right: 6px;
  border-right: @mediumBorder;
}
div.restOfHeader {
  display: inline-block;
  width: calc(100vw - 570px);
}
div.table {
  display: table;
  width: 100%;
}
div.row {
  display: table-row;
  width: 100%;
}

div.title {
  display: table-cell;
  text-align: center;
}
div.calendar {
  width: 260px;
  display: inline-block;
  vertical-align: bottom;
}
</style>
<style lang="less">
div.calendar input {
  width: 14em;
}
div.calendar .vc-text-sm {
  font-size: 12px;
}
</style>
