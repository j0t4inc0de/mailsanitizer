<template>
  <div class="relative min-h-screen pt-28 pb-16 px-4">
    <!-- Background glow orbs -->
    <div class="glow-orb-primary w-96 h-96 -top-48 left-1/4 fixed animate-float" />
    <div class="glow-orb-accent w-72 h-72 bottom-20 -right-36 fixed animate-float-delayed" />
    <div class="glow-orb-secondary w-56 h-56 top-1/2 -left-28 fixed animate-float opacity-20" />

    <div class="mx-auto max-w-6xl">
      <!-- Header -->
      <div class="text-center mb-16">
        <div class="inline-flex items-center gap-2 rounded-full border border-brand-border bg-brand-glass px-4 py-1.5 text-sm text-brand-muted mb-6 backdrop-blur-sm">
          <svg class="w-4 h-4 text-brand-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          Los créditos nunca expiran
        </div>
        <h1 class="font-outfit text-4xl sm:text-5xl font-extrabold text-brand-text mb-4">
          Planes simples y <span class="gradient-text">transparentes</span>
        </h1>
        <p class="text-brand-muted text-lg max-w-xl mx-auto">
          Paga solo por lo que usas. Sin suscripciones mensuales. Compra créditos cuando los necesites.
        </p>
      </div>

      <!-- Pricing cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8 mb-16">
        <div
          v-for="plan in plans"
          :key="plan.name"
          class="relative flex flex-col rounded-2xl border p-8 transition-all duration-300"
          :class="plan.featured
            ? 'border-brand-primary/40 bg-brand-glass shadow-neon-primary md:-mt-6 md:mb-6 hover:shadow-[0_0_40px_rgba(139,92,246,0.4)]'
            : 'border-brand-border bg-brand-glass hover:border-brand-borderHover hover:shadow-neon-primary shadow-glass'"
          style="backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);"
        >
          <!-- Featured badge -->
          <div v-if="plan.featured" class="absolute -top-3.5 left-1/2 -translate-x-1/2">
            <span class="bg-brand-primary text-white text-xs font-bold px-5 py-1.5 rounded-full shadow-neon-primary">
              Más popular
            </span>
          </div>

          <!-- Plan header -->
          <div class="mb-6">
            <h3 class="font-outfit text-2xl font-bold text-brand-text mb-1">{{ plan.name }}</h3>
            <p class="text-brand-muted text-sm">{{ plan.tagline }}</p>
          </div>

          <!-- Price -->
          <div class="mb-2">
            <span class="font-outfit text-5xl font-extrabold text-brand-text">${{ plan.price }}</span>
            <span class="text-brand-muted text-sm ml-2">CLP</span>
          </div>

          <!-- Credits -->
          <div class="mb-6">
            <span class="text-brand-primary font-outfit font-bold text-lg">{{ plan.creditsFormatted }}</span>
            <span class="text-brand-muted text-sm ml-1">créditos</span>
          </div>

          <!-- Cost per email -->
          <div class="rounded-lg bg-white/[0.03] border border-brand-border px-4 py-2 mb-6">
            <span class="text-brand-muted text-xs">Costo por correo: </span>
            <span class="text-brand-text text-xs font-semibold">${{ plan.costPerEmail }} CLP</span>
          </div>

          <!-- Features -->
          <ul class="space-y-3 mb-8 flex-1">
            <li v-for="feat in plan.features" :key="feat" class="flex items-start gap-3 text-sm text-brand-muted">
              <svg class="w-4 h-4 text-brand-secondary flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>{{ feat }}</span>
            </li>
          </ul>

          <!-- CTA -->
          <a
            :href="plan.url"
            target="_blank"
            rel="noopener noreferrer"
            class="w-full text-center py-3.5"
            :class="plan.featured ? 'btn-primary text-base' : 'btn-secondary text-base'"
          >
            Comprar créditos
          </a>
        </div>
      </div>

      <!-- FAQ / Trust badges -->
      <div class="glass-panel p-8 sm:p-12">
        <h2 class="font-outfit text-2xl font-bold text-brand-text mb-8 text-center">
          Preguntas frecuentes
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="faq in faqs" :key="faq.q" class="space-y-2">
            <h3 class="font-outfit font-semibold text-brand-text flex items-start gap-2">
              <svg class="w-5 h-5 text-brand-primary flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ faq.q }}
            </h3>
            <p class="text-brand-muted text-sm pl-7">{{ faq.a }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const plans = [
  {
    name: 'Starter',
    tagline: 'Ideal para freelancers',
    price: '1.990',
    credits: 2000,
    creditsFormatted: '2.000',
    costPerEmail: '0.99',
    features: [
      '2.000 créditos de validación',
      'Validación sintaxis + DNS + SMTP',
      'Detección de correos desechables',
      'Descarga CSV limpio',
      'Los créditos nunca expiran',
    ],
    featured: false,
    url: 'https://wearesamod.lemonsqueezy.com/checkout/buy/3eb225d2-7a51-48ef-ad40-d57f2335782e',
  },
  {
    name: 'Pro',
    tagline: 'Para agencias pequeñas',
    price: '4.990',
    credits: 10000,
    creditsFormatted: '10.000',
    costPerEmail: '0.49',
    features: [
      '10.000 créditos de validación',
      'Todo lo del plan Starter',
      'Diagnóstico detallado por lista',
      'Soporte prioritario por email',
      'Los créditos nunca expiran',
    ],
    featured: true,
    url: 'https://wearesamod.lemonsqueezy.com/checkout/buy/c6cb9e2c-a4cc-45ef-a698-e55b72e0e4f7',
  },
  {
    name: 'Agency',
    tagline: 'Para equipos de marketing',
    price: '9.900',
    credits: 30000,
    creditsFormatted: '30.000',
    costPerEmail: '0.33',
    features: [
      '30.000 créditos de validación',
      'Todo lo del plan Pro',
      'API de validación incluida',
      'Webhook de resultados',
      'Suscripción mensual',
    ],
    featured: false,
    url: 'https://wearesamod.lemonsqueezy.com/checkout/buy/3efb4d37-3627-4c34-87da-738a66675d3a',
  },
]

const faqs = [
  {
    q: '¿Qué es un crédito?',
    a: 'Un crédito equivale a la validación de un correo electrónico. Si subes una lista con 50 correos, se usan 50 créditos.',
  },
  {
    q: '¿Los créditos expiran?',
    a: 'No, tus créditos nunca expiran. Los puedes usar cuando quieras, sin límite de tiempo.',
  },
  {
    q: '¿Qué incluye la validación?',
    a: 'Verificamos la sintaxis del correo, la existencia del dominio DNS, la conectividad SMTP, y detectamos dominios desechables.',
  },
  {
    q: '¿Puedo probar antes de comprar?',
    a: 'Al crear tu cuenta recibes 50 créditos gratis automáticamente para probar el servicio. No necesitas tarjeta de crédito para empezar.',
  },
  {
    q: '¿Qué métodos de pago aceptan?',
    a: 'Aceptamos tarjetas de crédito/débito y PayPal a través de Lemon Squeezy, nuestra plataforma de pagos segura.',
  },
  {
    q: '¿Puedo obtener un reembolso?',
    a: 'Ofrecemos una garantía de reembolso de 14 días para cualquier paquete de créditos que no haya sido utilizado. Consulta nuestra Política de Reembolso para más información.',
  },
]
</script>
