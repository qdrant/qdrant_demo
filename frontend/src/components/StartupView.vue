<template>
  <q-card class="my-card" flat bordered>
    <q-card-section horizontal>
      <q-card-section class="q-pt-xs">
        <div class="text-overline">{{ city }}</div>
        <div class="text-h6 q-mt-sm q-mb-xs">
          {{ name }}  <a :href="link" target="_blank"><q-icon name="open_in_new" /></a>
        </div>
        <div class="text-caption text-grey" v-html="description">
        </div>
      </q-card-section>

      <q-card-section class="col-5 flex flex-center">
        <q-img
          class="rounded-borders"
          :title="alt"
          :alt="alt"
          :src="startup_image"
        />
      </q-card-section>

    </q-card-section>
          <q-separator />
      <q-card-actions>
        <q-btn flat @click="select">Find similar</q-btn>
      </q-card-actions>
  </q-card>
</template>

<script>
export default {
  props: ["name", "description", "images", "link", "city", "alt"],
  computed: {
    startup_image() {
      if (this.images === "/img/spacer.gif") {
        return "/empty.jpg";
      }
      return this.images.replace('thumb_jpg', 'medium_jpg');
    },
  },
  methods: {
    select() {
      this.$emit("select")
    }
  }
};
</script>

<style>
</style>