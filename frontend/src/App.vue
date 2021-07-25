<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-brand-primary text-white">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          aria-label="Menu"
          icon="menu"
        />

        
        <img src="./assets/logo_v3.png" width="38px">
        

        <q-toolbar-title>Qdrant Demo</q-toolbar-title>

      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-2"
    >
      <q-list>
        <q-item-label header>Essential Links</q-item-label>
        <q-item clickable tag="a" target="_blank" href="https://qdrant.github.io/qdrant/redoc/index.html">
          <q-item-section avatar>
            <q-icon name="school" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Docs</q-item-label>
            <q-item-label caption>ReDoc OpenAPI v3.0</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable tag="a" target="_blank" href="https://github.com/qdrant/qdrant_demo">
          <q-item-section avatar>
            <q-icon name="code" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Github - Demo</q-item-label>
            <q-item-label caption>github.com/qdrant/qdrant_demo</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable tag="a" target="_blank" href="https://github.com/qdrant/qdrant">
          <q-item-section avatar>
            <q-icon name="code" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Github - Engine</q-item-label>
            <q-item-label caption>github.com/qdrant/qdrant</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable tag="a" target="_blank" href="https://t.me/neural_network_engineering">
          <q-item-section avatar>
            <q-icon name="chat" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Telegram Channel</q-item-label>
            <q-item-label caption>Neural Networks Engineering</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <Ribbon
      v-bind="ribbonOptions"
    ></Ribbon>

    <q-page-container>
      <router-view></router-view>
    </q-page-container>
  </q-layout>
</template>

<script>

export default {
  name: 'LayoutDefault',

  components: {
  },

  data () {
    return {
      leftDrawerOpen: false,
      ribbonOptions: {
        text: 'Fork me on GitHub',
        linkUrl: "https://github.com/qdrant/qdrant_demo",
        fixed: true,
        border: false
      }
    }
  }
}
</script>

<style>
.text-brand-primary {
  color: white;
}

.bg-brand-primary {
  background: #182b3a !important;
}
</style>
