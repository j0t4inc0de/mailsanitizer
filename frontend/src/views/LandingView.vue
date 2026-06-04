<template>
  <div class="relative overflow-hidden">
    <!-- Background glow orbs -->
    <div class="glow-orb-primary w-96 h-96 -top-48 -left-48 animate-float fixed" />
    <div class="glow-orb-accent w-80 h-80 top-1/3 -right-40 animate-float-delayed fixed" />
    <div class="glow-orb-secondary w-64 h-64 bottom-20 left-1/4 animate-float fixed opacity-20" />

    <!-- ─── HERO ─────────────────────────────────────────────── -->
    <section class="relative pt-32 pb-16 sm:pt-40 sm:pb-24 px-4">
      <div class="mx-auto max-w-5xl text-center">
        <h1 class="font-outfit text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold leading-tight tracking-tight mb-6 animate-slide-up">
          Limpia tu lista de correos
          <br />
          <span class="gradient-text">en segundos</span>
        </h1>

        <p class="mx-auto max-w-2xl text-lg sm:text-xl text-brand-muted leading-relaxed mb-10 animate-slide-up animate-delay-200">
          Elimina correos inválidos, desechables y riesgosos antes de enviar tu campaña.
          Mejora tu deliverability y protege tu reputación de envío.
        </p>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up animate-delay-400">
          <router-link to="/pricing" class="btn-primary text-lg py-4 px-8">
            Empieza gratis — 500 créditos incluidos
          </router-link>
          <a href="#como-funciona" class="btn-ghost text-lg">
            ¿Cómo funciona?
          </a>
        </div>
      </div>
    </section>

    <!-- ─── SINGLE VALIDATOR (Lead Magnet) ───────────────────── -->
    <section class="relative py-16 px-4">
      <div class="mx-auto max-w-2xl animate-slide-up animate-delay-600">
        <SingleValidator />
      </div>
    </section>

    <!-- ─── HOW IT WORKS ─────────────────────────────────────── -->
    <section id="como-funciona" class="relative py-20 sm:py-28 px-4">
      <div class="mx-auto max-w-6xl">
        <div class="text-center mb-16">
          <h2 class="font-outfit text-3xl sm:text-4xl font-bold text-brand-text mb-4">
            ¿Cómo funciona?
          </h2>
          <p class="text-brand-muted text-lg max-w-xl mx-auto">
            Tres pasos simples para limpiar tu lista de correos
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
          <!-- Step 1 -->
          <div class="glass-panel-hover p-8 text-center group">
            <div class="w-16 h-16 mx-auto mb-5 rounded-2xl bg-brand-primary/10 border border-brand-primary/20 flex items-center justify-center group-hover:shadow-neon-primary transition-all duration-300">
              <svg class="w-8 h-8 text-brand-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <div class="text-brand-primary/40 font-outfit text-5xl font-black mb-3">01</div>
            <h3 class="font-outfit text-xl font-bold text-brand-text mb-2">Sube tu lista CSV</h3>
            <p class="text-brand-muted text-sm leading-relaxed">
              Arrastra y suelta tu archivo CSV con la lista de correos que deseas validar.
            </p>
          </div>

          <!-- Step 2 -->
          <div class="glass-panel-hover p-8 text-center group">
            <div class="w-16 h-16 mx-auto mb-5 rounded-2xl bg-brand-accent/10 border border-brand-accent/20 flex items-center justify-center group-hover:shadow-neon-accent transition-all duration-300">
              <svg class="w-8 h-8 text-brand-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div class="text-brand-accent/40 font-outfit text-5xl font-black mb-3">02</div>
            <h3 class="font-outfit text-xl font-bold text-brand-text mb-2">Procesamos en segundos</h3>
            <p class="text-brand-muted text-sm leading-relaxed">
              Nuestro motor valida sintaxis, dominio DNS y conectividad SMTP en paralelo.
            </p>
          </div>

          <!-- Step 3 -->
          <div class="glass-panel-hover p-8 text-center group">
            <div class="w-16 h-16 mx-auto mb-5 rounded-2xl bg-brand-secondary/10 border border-brand-secondary/20 flex items-center justify-center group-hover:shadow-neon-secondary transition-all duration-300">
              <svg class="w-8 h-8 text-brand-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="text-brand-secondary/40 font-outfit text-5xl font-black mb-3">03</div>
            <h3 class="font-outfit text-xl font-bold text-brand-text mb-2">Descarga el reporte limpio</h3>
            <p class="text-brand-muted text-sm leading-relaxed">
              Obtén un CSV limpio sin correos problemáticos, listo para tu campaña de email.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── STATS ─────────────────────────────────────────────── -->
    <section class="relative py-20 px-4">
      <div class="mx-auto max-w-5xl">
        <div class="glass-panel p-10 sm:p-14">
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-8 text-center">
            <div>
              <div class="font-outfit text-4xl sm:text-5xl font-extrabold gradient-text mb-2">
                +{{ animatedEmails }}
              </div>
              <p class="text-brand-muted">correos validados</p>
            </div>
            <div>
              <div class="font-outfit text-4xl sm:text-5xl font-extrabold text-brand-secondary mb-2">
                {{ animatedAccuracy }}%
              </div>
              <p class="text-brand-muted">precisión</p>
            </div>
            <div>
              <div class="font-outfit text-4xl sm:text-5xl font-extrabold text-brand-accent mb-2">
                {{ animatedLayers }}
              </div>
              <p class="text-brand-muted">capas de verificación</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── PRICING PREVIEW ──────────────────────────────────── -->
    <section class="relative py-20 sm:py-28 px-4">
      <div class="mx-auto max-w-6xl">
        <div class="text-center mb-16">
          <h2 class="font-outfit text-3xl sm:text-4xl font-bold text-brand-text mb-4">
            Planes simples y transparentes
          </h2>
          <p class="text-brand-muted text-lg max-w-xl mx-auto">
            Paga solo por lo que usas. Los créditos nunca expiran.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
          <div
            v-for="plan in plans"
            :key="plan.name"
            class="relative glass-panel-hover p-8 flex flex-col"
            :class="plan.featured ? 'border-brand-primary/40 shadow-neon-primary md:-mt-4 md:mb-4' : ''"
          >
            <div v-if="plan.featured" class="absolute -top-3 left-1/2 -translate-x-1/2">
              <span class="bg-brand-primary text-white text-xs font-bold px-4 py-1 rounded-full shadow-neon-primary">
                Más popular
              </span>
            </div>

            <h3 class="font-outfit text-xl font-bold text-brand-text mb-1">{{ plan.name }}</h3>
            <p class="text-brand-muted text-sm mb-5">{{ plan.tagline }}</p>

            <div class="mb-6">
              <span class="font-outfit text-4xl font-extrabold text-brand-text">${{ plan.price }}</span>
              <span class="text-brand-muted text-sm ml-1">USD</span>
            </div>

            <ul class="space-y-3 mb-8 flex-1">
              <li v-for="feat in plan.features" :key="feat" class="flex items-start gap-2 text-sm text-brand-muted">
                <svg class="w-4 h-4 text-brand-secondary flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                {{ feat }}
              </li>
            </ul>

            <a
              :href="plan.url"
              class="w-full text-center"
              :class="plan.featured ? 'btn-primary' : 'btn-secondary'"
            >
              Comprar créditos
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── FINAL CTA ────────────────────────────────────────── -->
    <section class="relative py-20 sm:py-28 px-4">
      <div class="mx-auto max-w-3xl text-center">
        <h2 class="font-outfit text-3xl sm:text-4xl font-bold text-brand-text mb-4">
          ¿Listo para limpiar tu lista?
        </h2>
        <p class="text-brand-muted text-lg mb-8 max-w-xl mx-auto">
          Empieza gratis con 500 créditos. Sin tarjeta de crédito. Sin compromiso.
        </p>
        <router-link to="/pricing" class="btn-primary text-lg py-4 px-10">
          Empezar ahora — Es gratis
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SingleValidator from '../components/SingleValidator.vue'

// Animated counters
const animatedEmails = ref('0')
const animatedAccuracy = ref('0')
const animatedLayers = ref(0)

function animateCounter(target, duration, setter, isFloat = false) {
  const start = performance.now()
  function step(now) {
    const progress = Math.min((now - start) / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3) // easeOutCubic
    const current = target * eased
    if (isFloat) {
      setter(current.toFixed(1))
    } else {
      setter(Math.floor(current).toLocaleString('es-CL'))
    }
    if (progress < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}

onMounted(() => {
  // Use intersection observer to trigger when visible
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(50000, 2000, (v) => (animatedEmails.value = v))
          animateCounter(99.2, 2000, (v) => (animatedAccuracy.value = v), true)
          animateCounter(3, 1500, (v) => (animatedLayers.value = Math.round(parseFloat(v))))
          observer.disconnect()
        }
      })
    },
    { threshold: 0.3 }
  )

  // Observe stats section
  setTimeout(() => {
    const statsSection = document.querySelectorAll('section')[3]
    if (statsSection) observer.observe(statsSection)
  }, 100)
})

// Pricing plans
const plans = [
  {
    name: 'Starter',
    tagline: 'Ideal para freelancers',
    price: '1.99',
    features: [
      '2.000 créditos de validación',
      'Validación sintaxis + DNS + SMTP',
      'Detección de correos desechables',
      'Descarga CSV limpio',
      'Los créditos nunca expiran',
    ],
    featured: false,
    url: 'https://cleanmail.lemonsqueezy.com/buy/starter',
  },
  {
    name: 'Pro',
    tagline: 'Para agencias pequeñas',
    price: '4.99',
    features: [
      '10.000 créditos de validación',
      'Todo lo del plan Starter',
      'Diagnóstico detallado por lista',
      'Soporte prioritario por email',
      'Los créditos nunca expiran',
    ],
    featured: true,
    url: 'https://cleanmail.lemonsqueezy.com/buy/pro',
  },
  {
    name: 'Agency',
    tagline: 'Para equipos de marketing',
    price: '9.99',
    features: [
      '30.000 créditos de validación',
      'Todo lo del plan Pro',
      'API de validación incluida',
      'Webhook de resultados',
      'Los créditos nunca expiran',
    ],
    featured: false,
    url: 'https://cleanmail.lemonsqueezy.com/buy/agency',
  },
]
</script>
