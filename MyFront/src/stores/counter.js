import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }
  // ===================================================
  const active = ref("third")
  const changeActive = (val)=>{
    active.value = val
  }
  // -------------
  const data = ref([
    {name:"contain--1"},
    {name:"contain--2"},
    {name:"contain--3"},
    {name:"contain--4"},
  ])

  return { count, doubleCount, increment,active,changeActive, data }
})
