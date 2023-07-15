<template>
    <div class="h-full pt-4 sm:pt-16">
        <div>
            <div class="px-4 py-8 mx-auto bg-white sm:mt-6 sm:w-0112 sm:w-96 sm:px-10 sm:rounded-lg sm:shadow-xl">
                <div class="mb-6 text-center">
                    <span class="text-lg">{{ title }}</span>
                </div>
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'LoginBox',
    props: {
        title: {
            type: String,
            required: true,
        },
    },
}
</script>
