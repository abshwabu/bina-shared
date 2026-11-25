<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'
import { useToast } from '@/composables/useToast'
import {
  Crown,
  Zap,
  Layers,
  CheckCircle2,
  AlertOctagon,
  ShieldCheck,
  Clock,
  Sparkles,
  X,
  ArrowLeft,
  Copy,
  Check,
  CreditCard,
  Building2,
  Phone,
  User,
  FileText,
  RefreshCw,
  AlertCircle,
  Smartphone,
} from '@lucide/vue'
import UiButton from '@/components/ui/UiButton.vue'
import UiSpinner from '@/components/ui/UiSpinner.vue'

const props = withDefaults(
  defineProps<{
    modelValue?: boolean
    forced?: boolean
  }>(),
  {
    modelValue: false,
    forced: false,
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'plan-selected', plan: any): void
}>()

const authStore = useAuthStore()
const toast = useToast()

const currentStep = ref<'select' | 'payment' | 'pending'>('select')
const billingCycle = ref<'monthly' | 'annually'>('monthly')
const isLoading = ref(false)
const isSubmitting = ref(false)
const isCheckingStatus = ref(false)
const copiedKey = ref<string | null>(null)

const selectedPlan = ref<any | null>(null)
const plans = ref<any[]>([])

// Payment Confirmation Form
const paymentForm = ref({
  payment_method: 'telebirr',
  payment_reference: '',
  payer_name: '',
  payer_phone: '',
  notes: '',
})

// Ethiopian Payment Options Reference
const paymentAccounts = [
  {
    key: 'telebirr',
    name: 'Telebirr SuperApp',
    type: 'Mobile Money',
    accountName: 'Bina Cloud Technologies (ERP)',
    accountNumber: '0911223344',
    badge: 'Instant Receipt',
    instructions: 'Send money or transfer via Telebirr merchant/number, then enter transaction ID below.',
  },
  {
    key: 'cbe_transfer',
    name: 'Commercial Bank of Ethiopia (CBE)',
    type: 'Bank Transfer / CBE Birr',
    accountName: 'Bina Cloud Technologies PLC',
    accountNumber: '1000123456789',
    badge: 'Direct Deposit',
    instructions: 'Transfer via CBE Mobile Banking or branch deposit, and provide transaction reference.',
  },
  {
    key: 'awash_bank',
    name: 'Awash Bank',
    type: 'Bank Transfer',
    accountName: 'Bina Cloud Technologies PLC',
    accountNumber: '01320876543200',
    badge: 'Direct Deposit',
    instructions: 'Deposit or transfer using Awash Online / Mobile Banking, enter slip reference.',
  },
  {
    key: 'cbe_birr',
    name: 'CBE Birr',
    type: 'Mobile Wallet',
    accountName: 'Bina Cloud ERP',
    accountNumber: '0911223344',
    badge: 'Mobile Wallet',
    instructions: 'Pay through CBE Birr wallet and enter the confirmation SMS reference.',
  },
]

const isDismissed = ref(false)

const closeModal = () => {
  isDismissed.value = true
  emit('update:modelValue', false)
}

const isOpen = computed({
  get: () => !isDismissed.value && (props.forced || props.modelValue),
  set: (val: boolean) => {
    if (!val) {
      closeModal()
    } else {
      isDismissed.value = false
      emit('update:modelValue', true)
    }
  },
})

// Listen to Escape key to close popup
const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && isOpen.value) {
    closeModal()
  }
}

// Reset dismissed flag whenever modelValue is explicitly set to true
watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      isDismissed.value = false
    }
  }
)

const existingPendingRequest = computed(() => {
  return authStore.subscriptionRequest || authStore.user?.tenant?.subscription_request || null
})

const isPendingApproval = computed(() => {
  return authStore.isPendingActivation || existingPendingRequest.value?.status === 'pending'
})

// Watch for pending activation to auto-switch step
watch(
  [() => isOpen.value, isPendingApproval],
  ([open, pending]) => {
    if (open) {
      if (pending) {
        currentStep.value = 'pending'
      } else if (currentStep.value === 'pending') {
        currentStep.value = 'select'
      }
    }
  },
  { immediate: true }
)

const fetchPlans = async () => {
  isLoading.value = true
  try {
    const res = await authApi.getBillingPlans()
    plans.value = res.data || []
    if (plans.value.length > 0) {
      // Default select the most popular or enterprise plan
      const defaultPlan = plans.value.find((p) => p.slug === 'professional') || plans.value[0]
      selectedPlan.value = defaultPlan
    }
  } catch (err: any) {
    toast.error('Failed to load subscription plans: ' + (err?.response?.data?.message || err?.message))
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchPlans()

  // Pre-fill payer name from logged in user if available
  if (authStore.user?.name) {
    paymentForm.value.payer_name = authStore.user.name
  }

  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

const copyToClipboard = (text: string, key: string) => {
  navigator.clipboard.writeText(text)
  copiedKey.value = key
  toast.success(`Copied "${text}" to clipboard!`)
  setTimeout(() => {
    if (copiedKey.value === key) copiedKey.value = null
  }, 2500)
}

const proceedToPayment = (plan: any) => {
  selectedPlan.value = plan
  currentStep.value = 'payment'
}

const handleBackToSelect = () => {
  currentStep.value = 'select'
}

const calculatePriceBirr = (plan: any) => {
  if (!plan) return 0
  const cents = billingCycle.value === 'annually' ? plan.price_annually : plan.price_monthly
  return cents / 100
}

const submitPaymentConfirmation = async () => {
  if (!selectedPlan.value) {
    toast.error('Please choose a subscription plan first.')
    return
  }

  if (!paymentForm.value.payment_reference.trim()) {
    toast.error('Please provide your bank or Telebirr transaction reference number.')
    return
  }

  if (!paymentForm.value.payer_name.trim()) {
    toast.error('Please provide the payer full name.')
    return
  }

  if (!paymentForm.value.payer_phone.trim()) {
    toast.error('Please provide a contact phone number for payment verification.')
    return
  }

  isSubmitting.value = true
  try {
    const res = await authApi.selectPlan({
      plan_id: selectedPlan.value.id,
      billing_cycle: billingCycle.value,
      payment_method: paymentForm.value.payment_method,
      payment_reference: paymentForm.value.payment_reference.trim(),
      payer_name: paymentForm.value.payer_name.trim(),
      payer_phone: paymentForm.value.payer_phone.trim(),
      notes: paymentForm.value.notes.trim() || undefined,
    })

    toast.success(res.message || 'Payment confirmation submitted for Super Admin review!')
    emit('plan-selected', selectedPlan.value)

    // Refresh user state from backend
    await authStore.checkAuth()

    // Move to pending state
    currentStep.value = 'pending'
  } catch (err: any) {
    toast.error(err?.response?.data?.message || err?.message || 'Failed to submit payment confirmation.')
  } finally {
    isSubmitting.value = false
  }
}

const checkActivationStatus = async () => {
  isCheckingStatus.value = true
  try {
    await authStore.checkAuth()
    if (authStore.user?.tenant?.status === 'active') {
      toast.success('Your workspace subscription has been approved and activated by the Super Admin!')
      if (!props.forced) {
        emit('update:modelValue', false)
      }
    } else {
      toast.info('Your payment verification is currently in review by the Super Admin.')
    }
  } catch (err: any) {
    toast.error('Could not check status: ' + (err?.response?.data?.message || err?.message))
  } finally {
    isCheckingStatus.value = false
  }
}
</script>

<template>
  <!-- Full Screen / Modal Overlay -->
  <div
    v-if="isOpen"
    @click.self="closeModal"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/80 backdrop-blur-md overflow-y-auto"
  >
    <div
      class="bg-white rounded-3xl border border-slate-200 shadow-2xl w-full max-w-5xl my-8 overflow-hidden flex flex-col relative transition-all"
      :class="props.forced ? 'ring-4 ring-amber-500/20' : ''"
    >
      <!-- Top Right Close button (Always accessible across all steps) -->
      <button
        @click="closeModal"
        type="button"
        class="absolute top-5 right-5 p-2 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors z-30 cursor-pointer flex items-center gap-1.5 group"
        title="Close (Esc)"
        aria-label="Close"
      >
        <span class="text-xs font-semibold text-slate-400 group-hover:text-slate-700 hidden sm:inline">Close</span>
        <X class="w-5 h-5" />
      </button>

      <!-- ── STEP 1: PLAN SELECTION ─────────────────────────────────────────── -->
      <div v-if="currentStep === 'select'">
        <!-- Banner Header -->
        <div
          class="p-6 lg:p-8 text-center space-y-3"
          :class="props.forced ? 'bg-gradient-to-b from-amber-500/10 to-transparent' : 'bg-slate-50/50'"
        >
          <div v-if="props.forced" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-100 text-amber-900 text-xs font-bold border border-amber-200 shadow-xs">
            <AlertOctagon class="w-4 h-4 text-amber-600" />
            <span>Your 2-Month Free Trial Has Ended</span>
          </div>

          <div v-else class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-50 text-indigo-700 text-xs font-bold border border-indigo-100">
            <Sparkles class="w-4 h-4 text-indigo-600" />
            <span>Choose Your Workspace Subscription</span>
          </div>

          <h2 class="text-2xl lg:text-3xl font-black text-slate-900 tracking-tight">
            {{ props.forced ? 'Select a Plan to Continue Operations' : 'Upgrade Your ERP Capabilities' }}
          </h2>

          <p class="text-sm text-slate-500 max-w-2xl mx-auto leading-relaxed">
            {{
              props.forced
                ? 'Your organization has enjoyed 60 days of enterprise cloud ERP. Select a subscription tier in Ethiopian Birr and submit your payment confirmation for Super Admin activation.'
                : 'Select the optimal operational tier for your team. All pricing is billed in Ethiopian Birr (ETB). Subscriptions are activated upon Super Admin payment confirmation.'
            }}
          </p>

          <!-- Billing Cycle Toggle -->
          <div class="pt-2 flex justify-center">
            <div class="inline-flex items-center p-1 bg-slate-200/70 rounded-2xl text-xs font-bold">
              <button
                type="button"
                @click="billingCycle = 'monthly'"
                class="px-4 py-1.5 rounded-xl transition-all cursor-pointer"
                :class="billingCycle === 'monthly' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'"
              >
                Billed Monthly
              </button>
              <button
                type="button"
                @click="billingCycle = 'annually'"
                class="px-4 py-1.5 rounded-xl transition-all flex items-center gap-1.5 cursor-pointer"
                :class="billingCycle === 'annually' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'"
              >
                <span>Billed Annually</span>
                <span class="px-1.5 py-0.2 rounded-md bg-emerald-100 text-emerald-800 text-[10px] font-black uppercase">
                  Save ~17%
                </span>
              </button>
            </div>
          </div>
        </div>

        <!-- Plan Cards Container -->
        <div class="p-6 lg:p-8 pt-0">
          <div v-if="isLoading" class="p-16 flex justify-center">
            <UiSpinner size="lg" />
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div
              v-for="plan in plans"
              :key="plan.id"
              class="rounded-3xl border p-6 flex flex-col justify-between space-y-6 relative transition-all duration-200 hover:shadow-lg"
              :class="[
                plan.slug === 'enterprise' ? 'border-purple-300 ring-2 ring-purple-600/30 bg-purple-50/10' :
                plan.slug === 'professional' ? 'border-blue-300 ring-2 ring-blue-600/30 bg-blue-50/10' :
                'border-slate-200 bg-white'
              ]"
            >
              <!-- Badge -->
              <div
                v-if="plan.badge"
                class="absolute top-0 right-0 font-bold text-[10px] px-3 py-1 rounded-bl-xl uppercase tracking-wider text-white"
                :class="[
                  plan.slug === 'enterprise' ? 'bg-gradient-to-r from-purple-600 to-indigo-600' :
                  plan.slug === 'professional' ? 'bg-gradient-to-r from-blue-600 to-cyan-600' :
                  'bg-slate-700'
                ]"
              >
                {{ plan.badge }}
              </div>

              <div class="space-y-4">
                <div class="flex items-center gap-2">
                  <Crown v-if="plan.slug === 'enterprise'" class="w-5 h-5 text-amber-500" />
                  <Zap v-else-if="plan.slug === 'professional'" class="w-5 h-5 text-blue-500" />
                  <Layers v-else class="w-5 h-5 text-slate-500" />
                  <h3 class="text-xl font-black text-slate-900">{{ plan.name }}</h3>
                </div>

                <p class="text-xs text-slate-500 leading-relaxed min-h-[36px]">
                  {{ plan.tagline || plan.description }}
                </p>

                <!-- Price -->
                <div class="p-4 bg-slate-50/80 rounded-2xl border border-slate-100 space-y-1">
                  <div class="flex items-baseline gap-1.5">
                    <span class="text-3xl font-black text-slate-900">
                      {{
                        billingCycle === 'monthly'
                          ? (plan.price_monthly / 100).toLocaleString()
                          : (plan.price_annually / 100 / 12).toFixed(0)
                      }}
                    </span>
                    <span class="text-sm font-bold text-slate-700">Birr</span>
                    <span class="text-xs text-slate-500 font-medium">/ month</span>
                  </div>
                  <div class="text-[11px] text-slate-400 font-medium">
                    {{
                      billingCycle === 'monthly'
                        ? 'Billed monthly per organization'
                        : `${(plan.price_annually / 100).toLocaleString()} Birr billed annually`
                    }}
                  </div>
                </div>

                <!-- Perks -->
                <div class="space-y-2 pt-2 border-t border-slate-100">
                  <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                    Included Perks & Features
                  </span>
                  <ul class="space-y-2 text-xs text-slate-700">
                    <li
                      v-for="(perk, i) in plan.perks.slice(0, 7)"
                      :key="i"
                      class="flex items-start gap-2 leading-snug"
                    >
                      <CheckCircle2 class="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                      <span :class="perk.startsWith('Everything in') ? 'font-bold text-indigo-700' : ''">{{ perk }}</span>
                    </li>
                  </ul>
                </div>
              </div>

              <!-- Action Button: Proceed to Payment Confirmation -->
              <div class="pt-4 border-t border-slate-100">
                <UiButton
                  class="w-full font-bold shadow-xs cursor-pointer"
                  :variant="plan.slug === 'professional' ? 'primary' : plan.slug === 'enterprise' ? 'primary' : 'outline'"
                  @click="proceedToPayment(plan)"
                >
                  Choose {{ plan.name }} & Pay
                </UiButton>
              </div>
            </div>
          </div>
        </div>

        <!-- Trust Footer & Dismiss -->
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
          <div class="flex items-center gap-2">
            <ShieldCheck class="w-4 h-4 text-emerald-600" />
            <span>Secure Multi-Tenant SQLite Isolation & Architecture</span>
          </div>
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-1.5">
              <Clock class="w-4 h-4 text-blue-600" />
              <span>Payment Verified & Activated by Super Admin</span>
            </div>
            <button
              type="button"
              @click="closeModal"
              class="font-bold text-slate-600 hover:text-slate-900 underline transition-colors cursor-pointer"
            >
              Close / Dismiss
            </button>
          </div>
        </div>
      </div>

      <!-- ── STEP 2: PAYMENT INSTRUCTIONS & CONFIRMATION ──────────────────────── -->
      <div v-else-if="currentStep === 'payment'" class="p-6 lg:p-8 space-y-6">
        <!-- Header with Back Button -->
        <div class="flex items-center justify-between border-b border-slate-100 pb-4">
          <button
            type="button"
            @click="handleBackToSelect"
            class="inline-flex items-center gap-2 text-xs font-bold text-slate-600 hover:text-slate-900 transition-colors cursor-pointer"
          >
            <ArrowLeft class="w-4 h-4" />
            <span>Back to Plan Options</span>
          </button>

          <span class="px-3 py-1 bg-amber-50 text-amber-800 rounded-full text-xs font-bold border border-amber-200">
            Step 2: Confirm Payment Details
          </span>
        </div>

        <!-- Selected Tier Summary Banner -->
        <div class="bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-md">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="text-xs uppercase font-extrabold tracking-wider text-indigo-300">Selected Plan</span>
              <span class="px-2 py-0.5 rounded-md bg-white/20 text-[11px] font-bold uppercase">{{ billingCycle }}</span>
            </div>
            <h3 class="text-xl font-black text-white flex items-center gap-2">
              {{ selectedPlan?.name }} Plan
            </h3>
            <p class="text-xs text-slate-300">
              {{ selectedPlan?.tagline || 'Enterprise ERP Suite with Multi-User & Multi-Warehouse capabilities' }}
            </p>
          </div>

          <div class="text-right sm:border-l sm:border-white/10 sm:pl-6 shrink-0">
            <div class="text-xs text-slate-400">Total Payable Amount</div>
            <div class="text-3xl font-black text-amber-400">
              {{ calculatePriceBirr(selectedPlan).toLocaleString() }} <span class="text-sm font-bold text-white">ETB</span>
            </div>
            <div class="text-[11px] text-slate-400">
              {{ billingCycle === 'annually' ? 'Billed annually (12 months)' : 'Billed for 1 month access' }}
            </div>
          </div>
        </div>

        <!-- 2-Column Layout: Bank Accounts List & Payment Form -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <!-- Left: Ethiopian Payment Accounts -->
          <div class="lg:col-span-5 space-y-4">
            <div class="flex items-center gap-2 text-sm font-bold text-slate-900">
              <Building2 class="w-4 h-4 text-indigo-600" />
              <span>Official Deposit Accounts (Ethiopia)</span>
            </div>
            <p class="text-xs text-slate-500">
              Transfer the exact subscription amount to any of the accounts below, then enter your confirmation reference:
            </p>

            <div class="space-y-3">
              <div
                v-for="acc in paymentAccounts"
                :key="acc.key"
                class="p-3.5 rounded-2xl border transition-all cursor-pointer"
                :class="paymentForm.payment_method === acc.key ? 'border-indigo-500 bg-indigo-50/20 ring-2 ring-indigo-500/20' : 'border-slate-200 bg-slate-50/60 hover:bg-slate-50'"
                @click="paymentForm.payment_method = acc.key"
              >
                <div class="flex items-center justify-between pb-1">
                  <div class="font-bold text-xs text-slate-900 flex items-center gap-1.5">
                    <Smartphone v-if="acc.type.includes('Mobile')" class="w-3.5 h-3.5 text-emerald-600" />
                    <Building2 v-else class="w-3.5 h-3.5 text-blue-600" />
                    {{ acc.name }}
                  </div>
                  <span class="text-[10px] font-bold px-2 py-0.5 rounded-md bg-white border border-slate-200 text-slate-600">
                    {{ acc.badge }}
                  </span>
                </div>

                <div class="text-xs text-slate-600 font-medium">
                  Name: <span class="font-bold text-slate-800">{{ acc.accountName }}</span>
                </div>

                <div class="mt-2 flex items-center justify-between bg-white px-2.5 py-1.5 rounded-xl border border-slate-200 font-mono text-xs">
                  <span class="font-bold text-slate-900">{{ acc.accountNumber }}</span>
                  <button
                    type="button"
                    @click.stop="copyToClipboard(acc.accountNumber, acc.key)"
                    class="p-1 text-slate-500 hover:text-indigo-600 transition-colors cursor-pointer"
                    title="Copy Account Number"
                  >
                    <Check v-if="copiedKey === acc.key" class="w-3.5 h-3.5 text-emerald-600" />
                    <Copy v-else class="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Payment Confirmation Form -->
          <div class="lg:col-span-7 bg-slate-50 rounded-2xl p-5 border border-slate-200 space-y-4">
            <div class="space-y-1">
              <h4 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                <CheckCircle class="w-4 h-4 text-emerald-600" />
                <span>Submit Proof of Transfer / Reference</span>
              </h4>
              <p class="text-xs text-slate-500">
                Our platform Super Admin will verify this transaction reference against the bank or Telebirr account statement and activate your workspace.
              </p>
            </div>

            <form @submit.prevent="submitPaymentConfirmation" class="space-y-4 pt-1">
              <!-- Payment Method Selection -->
              <div>
                <label class="block text-xs font-bold text-slate-700 mb-1">Payment Method Used *</label>
                <select
                  v-model="paymentForm.payment_method"
                  class="w-full text-xs font-medium bg-white border border-slate-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="telebirr">Telebirr (Mobile Money)</option>
                  <option value="cbe_transfer">Commercial Bank of Ethiopia (CBE Transfer)</option>
                  <option value="cbe_birr">CBE Birr (Mobile Wallet)</option>
                  <option value="awash_bank">Awash Bank Transfer</option>
                  <option value="bank_transfer">Other Ethiopian Bank Transfer</option>
                </select>
              </div>

              <!-- Transaction Reference Number -->
              <div>
                <label class="block text-xs font-bold text-slate-700 mb-1">
                  Transaction Reference / Deposit Slip / Voucher ID *
                </label>
                <input
                  v-model="paymentForm.payment_reference"
                  type="text"
                  required
                  placeholder="e.g. TLB8943729 or FT2628489248"
                  class="w-full text-xs font-mono font-medium bg-white border border-slate-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <span class="text-[11px] text-slate-400 mt-0.5 block">
                  Found on your Telebirr SMS confirmation or CBE transaction receipt slip.
                </span>
              </div>

              <!-- Payer Name & Phone in 2 Columns -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-bold text-slate-700 mb-1">Payer Full Name *</label>
                  <input
                    v-model="paymentForm.payer_name"
                    type="text"
                    required
                    placeholder="e.g. Abebe Kebede"
                    class="w-full text-xs bg-white border border-slate-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label class="block text-xs font-bold text-slate-700 mb-1">Payer Phone Number *</label>
                  <input
                    v-model="paymentForm.payer_phone"
                    type="text"
                    required
                    placeholder="e.g. 0911223344"
                    class="w-full text-xs bg-white border border-slate-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <!-- Optional Notes -->
              <div>
                <label class="block text-xs font-bold text-slate-700 mb-1">Additional Notes / Remarks (Optional)</label>
                <textarea
                  v-model="paymentForm.notes"
                  rows="2"
                  placeholder="e.g. Transferred from Awash account under Abebe K. PLC"
                  class="w-full text-xs bg-white border border-slate-200 rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                ></textarea>
              </div>

              <!-- Actions -->
              <div class="pt-2 flex items-center justify-end gap-3 border-t border-slate-200">
                <UiButton
                  type="button"
                  variant="outline"
                  size="sm"
                  @click="handleBackToSelect"
                >
                  Back
                </UiButton>

                <UiButton
                  type="button"
                  variant="ghost"
                  size="sm"
                  @click="closeModal"
                >
                  Close
                </UiButton>

                <UiButton
                  type="submit"
                  variant="primary"
                  size="sm"
                  class="font-bold shadow-xs cursor-pointer"
                  :loading="isSubmitting"
                >
                  Submit Payment Confirmation
                </UiButton>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- ── STEP 3: PENDING SUPER ADMIN ACTIVATION STATUS ───────────────────── -->
      <div v-else-if="currentStep === 'pending'" class="p-8 lg:p-12 text-center space-y-6">
        <div class="w-16 h-16 rounded-3xl bg-amber-100 text-amber-700 flex items-center justify-center mx-auto shadow-inner">
          <Clock class="w-8 h-8 animate-pulse text-amber-600" />
        </div>

        <div class="space-y-2 max-w-lg mx-auto">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-50 text-amber-800 text-xs font-bold border border-amber-200">
            <span class="w-2 h-2 rounded-full bg-amber-500 animate-ping"></span>
            <span>Awaiting Super Admin Verification</span>
          </div>

          <h3 class="text-2xl font-black text-slate-900 tracking-tight">
            Payment Confirmation Submitted
          </h3>

          <p class="text-xs text-slate-500 leading-relaxed">
            Thank you! Your payment verification request has been received. The platform Super Admin will verify your transaction reference against our bank/Telebirr records and activate your workspace.
          </p>
        </div>

        <!-- Request Summary Card -->
        <div class="max-w-md mx-auto bg-slate-50 border border-slate-200 rounded-2xl p-5 text-left space-y-3 text-xs">
          <div class="flex items-center justify-between pb-2 border-b border-slate-200/80">
            <span class="text-slate-500 font-medium">Requested Plan:</span>
            <span class="font-bold text-slate-900">
              {{ existingPendingRequest?.plan_name || selectedPlan?.name || 'Enterprise' }} Plan
              ({{ existingPendingRequest?.billing_cycle || billingCycle }})
            </span>
          </div>

          <div class="flex items-center justify-between pb-2 border-b border-slate-200/80">
            <span class="text-slate-500 font-medium">Payable Amount:</span>
            <span class="font-black text-indigo-700">
              {{ (existingPendingRequest?.amount_birr || calculatePriceBirr(selectedPlan)).toLocaleString() }} ETB
            </span>
          </div>

          <div class="flex items-center justify-between pb-2 border-b border-slate-200/80">
            <span class="text-slate-500 font-medium">Payment Method:</span>
            <span class="font-bold text-slate-900 capitalize">
              {{ (existingPendingRequest?.payment_method || paymentForm.payment_method).replace('_', ' ') }}
            </span>
          </div>

          <div class="flex items-center justify-between pb-2 border-b border-slate-200/80">
            <span class="text-slate-500 font-medium">Transaction Reference:</span>
            <span class="font-mono font-bold text-slate-900 bg-white px-2 py-0.5 rounded-md border border-slate-200">
              {{ existingPendingRequest?.payment_reference || paymentForm.payment_reference || 'N/A' }}
            </span>
          </div>

          <div class="flex items-center justify-between">
            <span class="text-slate-500 font-medium">Payer Contact:</span>
            <span class="font-medium text-slate-800">
              {{ existingPendingRequest?.payer_name || paymentForm.payer_name }}
              ({{ existingPendingRequest?.payer_phone || paymentForm.payer_phone }})
            </span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <UiButton
            variant="primary"
            size="sm"
            class="font-bold shadow-xs cursor-pointer"
            :loading="isCheckingStatus"
            @click="checkActivationStatus"
          >
            <RefreshCw class="w-3.5 h-3.5 mr-1.5" />
            Check Activation Status
          </UiButton>

          <UiButton
            variant="outline"
            size="sm"
            @click="currentStep = 'payment'"
          >
            Update Payment Reference
          </UiButton>

          <UiButton
            variant="ghost"
            size="sm"
            @click="closeModal"
          >
            Close / Dismiss
          </UiButton>
        </div>
      </div>
    </div>
  </div>
</template>