<template>
    <div>
        <!-- value changes based on what is input
        id is the id of the field to pass to form
        attributes has all the data we're looking for 
        ex1. value: id: field2 attributes: { "model_class": "ColumnListParameter", "name": "field2", "argument": null, "type": "data_column", "label": "and column", "help": "", "refresh_on_change": false, "optional": false, "hidden": false, "is_dynamic": true, "value": null, "options": [], "display": null, "multiple": false, "textable": false, "data_ref": "input2", "numerical": false, "default_value": null, "text_value": "None" }
        ex2. value: N id: mode attributes: { "model_class": "SelectToolParameter", "name": "mode", "argument": null, "type": "select", "label": "To find", "help": "See examples below for explanation of these options", "refresh_on_change": false, "optional": false, "hidden": false, "is_dynamic": false, "value": "N", "options": [ [ "Matching rows of 1st dataset", "N", false ], [ "Non Matching rows of 1st dataset", "V", false ] ], "display": null, "multiple": false, "textable": false, "default_value": "N", "text_value": "Matching rows of 1st dataset" } 
    -->
        <!-- value: {{ value }} id: {{ id }} attributes: {{ attributes }} -->
        <FormParameter
            v-if="attributes.is_workflow"
            :id="id"
            ref="params"
            v-model="currentValue"
            :data-label="title"
            :type="type"
            :attributes="attributes" />
        <b-alert v-else-if="optionList.length == 0" show variant="info">
            {{ error_text }}
        </b-alert>
        <multiselect
            v-else-if="optionList.length && !display"
            v-model="currentValue"
            deselect-label="Can't remove this value"
            track-by="0"
            :options="optionList"
            :searchable="this.attributes.searchable"
            :allow-empty="false">
            {{ currentValue }}>
        </multiselect>
        <b-form-group label="label" v-else-if="display == checkboxes">
            <b-form-checkbox-group
                v-model="currentSelected"
                :options="optionList"
                stacked></b-form-checkbox-group>
        </b-form-group>
    </div>
</template>

<script>
import { getGalaxyInstance } from "../../../app";
import FormParameter from "./FormParameter";
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import Multiselect from "vue-multiselect";

Vue.use(BootstrapVue);
export default {
    components: {
        FormParameter,
        Multiselect,
    },
    props: {
        value: {
            type: String,
            default: "",
        },
        type: {
            type: String,
            required: true,
        },
        id: {
            type: String,
            required: true,
        },
        attributes: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            readonly: this.attributes.readonly,
            multiple: this.attributes.multiple,
            optional: this.attributes.optional,
            onchange: this.attributes.onchange,
            individual: this.attributes.individual,
            textable: this.attributes.textable,
            alternateErrorText: null,
            selected: [],
        };
    },
    computed: {
        currentValue: {
            get() {
                return this.value;
            },
            set(val) {
                this.$emit("input", val);
            },
        },
        currentSelected: {
            get() {
                return this.selected;
            },
            set(val) {
                this.$emit("input", val);
            },
        },
        data() {
            return this.attributes.data;
        },
        optionList() {
            return [].concat(...this.attributes.options);
        },
        display() {
            return this.attributes.display;
        },
        error_text() {
            return this.alternateErrorText || this.attributes.error_text || "No options available";
        },
        label() {
            return this.attributes.label;
        },
    },
    created() {
        console.log("attributes == ", this.attributes);
        this.currentValue = this.optionList[0];
        if (this.attributes.type == "data_column") {
            this.alternateErrorText = "Missing columns in referenced dataset.";
        }
        const Galaxy = getGalaxyInstance();
        if (this.attributes.flavor == "workflow") {
            if (Galaxy.config.select_type_workflow_threshold == -1) {
                this.searchable = false;
            } else if (Galaxy.config.select_type_workflow_threshold == 0) {
                this.searchable = true;
            } else if (Galaxy.config.select_type_workflow_threshold < this.attributes.options.length) {
                this.searchable = false;
            }
        }
    },
};
</script>
