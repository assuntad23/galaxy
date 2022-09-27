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
        <b-alert v-else-if="optionSelect.length == 0" show variant="info">
            {{ error_text }}
        </b-alert>
        <multiselect
            v-else-if="optionSelect.length"
            v-model="initialOption"
            deselect-label="Can't remove this value"
            track-by="first"
            label="first"
            :options="optionSelect"
            :searchable="true"
            :allow-empty="false">
            {{ initialOption }}>
        </multiselect>
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
            SelectClass: null,
            alternateErrorText: null,
        };
    },
    computed: {
        data() {
            return this.attributes.data;
        },
        optionSelect() {
            const arrayOfObjects = [];
            for (let index = 0; index < this.attributes.options.length; index++) {
                const obj = { first: this.attributes.options[index][0], second: this.attributes.options[index][1], third: this.attributes.options[index][2]} 
                arrayOfObjects.push(obj);
            }
            return arrayOfObjects;
        },
        display() {
            return this.attributes.display;
        },
        error_text() {
            return this.alternateErrorText || this.attributes.error_text || "No options available";
        },
        initialOption() {
            return this.optionSelect[0];
        },
    },
    created() {
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
        var classes = {
            checkboxes: "checkbox",
            radio: "radio",
            radiobutton: "radiobutton",
        };
        this.SelectClass = classes[this.attributes.display] || "select";
    },
};
</script>