<template>
    <div ref="container" class="scrollContainer">
        <div
            v-infinite-scroll="getMoreContent"
            infinite-scroll-disabled="busy"
            infinite-scroll-distance="0"
            :class="{ loadingBackground: loading, listing: true }"
        >
            <div v-for="(item, index, rowKey) in getData" :key="rowKey">
                <HistoryContentItem
                    :item="item"
                    :index="index"
                    :row-key="rowKey"
                    :show-selection="showSelection"
                    :expanded="isExpanded(item)"
                    @update:expanded="setExpanded(item, $event)"
                    :selected="isSelected(item)"
                    @update:selected="setSelected(item, $event)"
                    @viewCollection="$emit('viewCollection', item)"
                    :data-hid="item.hid"
                    :data-index="index"
                    :data-row-key="rowKey"
                />
            </div>
        </div>
    </div>
</template>
<script>
import { HistoryContentItem } from "./ContentItem";
import infiniteScroll from "vue-infinite-scroll";
import { setTimeout } from "timers";
export default {
    directives: { infiniteScroll },
    components: {
        HistoryContentItem,
    },
    data() {
        return {
            initialLoad: true,
            data: [],
            count: 0,
        };
    },
    computed: {
        getData() {
            console.log("DATA SIZE:", this.data.length);
            console.log("MORE DATA TIMES: ",this.count);
            return this.data;
        },
    },
    props: {
        setScrollPos: { type: Function, required: true },
        payload: { required: true },
        showSelection: { type: Function, required: true },
        isExpanded: { type: Function, required: true },
        setExpanded: { type: Function, required: true },
        isSelected: { type: Function, required: true },
        setSelected: { type: Function, required: true },
    },
    methods: {
        getMoreContent() {
            this.busy = true;

            // if (this.initialLoad == true) {
            //     this.data.push(this.payload.contents);
            //     this.initialLoad = false;
            // }
            // console.log("PAYLOAD ", this.payload);
            // console.log("HERE: ", this.payload.contents.length, this.payload.totalMatches);
            setTimeout(() => {
                this.data.push(...this.payload.contents);
                const pload = { cursor: this.getData.length / this.payload.totalMatches };
                console.log("MATH: ", this.getData.length, "/", this.payload.totalMatches, "=", pload);
                this.setScrollPos(pload);
                this.count++; 
                this.busy = false;
            }, 2000);
        },
    },
};
</script>

<style lang="scss">
@import "scss/mixins.scss";
.scrollContainer {
    .listing {
        overflow-y: scroll;
        z-index: 0;
    }
}
</style>
