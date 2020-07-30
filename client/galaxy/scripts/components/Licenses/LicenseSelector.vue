<template>
    <div class="btn-group dropdown">
        <button
            type="button"
            v-b-tooltip.hover.bottom
            :title="titleFilterMenu"
            class="rule-menu-filter-button primary-button dropdown-toggle"
            data-toggle="dropdown"
        >
            <span class="fa fa-plus"></span>
            {{ l("Filter") }}
            <span class="caret"></span>
        </button>
        <div class="dropdown-menu" role="menu">
            <rule-target-component :builder="this" rule-type="add_filter_regex" />
            <rule-target-component :builder="this" rule-type="add_filter_matches" />
            <rule-target-component :builder="this" rule-type="add_filter_compare" />
            <rule-target-component :builder="this" rule-type="add_filter_empty" />
            <rule-target-component :builder="this" rule-type="add_filter_count" />
        </div>
    </div>
</template>

<script>
export default {};
</script>
