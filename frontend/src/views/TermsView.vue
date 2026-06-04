<template>
  <div class="relative min-h-screen pt-28 pb-16 px-4">
    <!-- Background glow orbs -->
    <div class="glow-orb-primary w-96 h-96 -top-48 left-1/4 fixed animate-float" />
    <div class="glow-orb-accent w-72 h-72 bottom-20 -right-36 fixed animate-float-delayed" />

    <div class="mx-auto max-w-3xl">
      <!-- Back link -->
      <router-link to="/" class="inline-flex items-center gap-2 text-brand-muted hover:text-brand-text text-sm transition-colors mb-8">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Volver al inicio
      </router-link>

      <!-- Document structure -->
      <div class="glass-panel p-8 sm:p-12 relative z-10">
        <h1 class="font-outfit text-3xl sm:text-4xl font-extrabold text-brand-text mb-2">
          Términos de Servicio
        </h1>
        <p class="text-brand-muted text-sm mb-8">
          Última actualización: 04 de junio, 2026
        </p>

        <div class="space-y-6 text-brand-muted text-sm leading-relaxed">
          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">1. Aceptación de los Términos</h2>
            <p>
              Al acceder o utilizar la plataforma CleanMail by Samod (en adelante, "el Servicio"), operada bajo la representación de We Are Samod, aceptas cumplir y estar sujeto a estos Términos de Servicio. Si no estás de acuerdo con alguna parte de los términos, no podrás acceder a nuestros servicios.
            </p>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">2. Descripción del Servicio</h2>
            <p>
              CleanMail es una herramienta de software como servicio (SaaS) que proporciona validación e higiene de listas de correo electrónico. El servicio analiza las direcciones de correo proporcionadas para verificar su existencia, identificar dominios desechables, detectar trampas de spam y servidores de captura todo (catch-all), con el fin de optimizar las campañas de email marketing de nuestros clientes.
            </p>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">3. Uso Aceptable del Servicio</h2>
            <p>
              Te comprometes a utilizar el Servicio únicamente con fines lícitos y de acuerdo con estos Términos. Queda estrictamente prohibido:
            </p>
            <ul class="list-disc pl-5 space-y-1">
              <li>Utilizar el servicio para validar listas de correos obtenidas de forma ilegal o sin el consentimiento explícito de los destinatarios.</li>
              <li>Intentar saturar, hackear o interferir con la infraestructura tecnológica de la plataforma.</li>
              <li>Revender o redistribuir nuestros servicios de validación masiva sin autorización previa por escrito.</li>
              <li>Procesar información que infrinja leyes de privacidad o derechos de terceros.</li>
            </ul>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">4. Cuentas, Créditos y Pagos</h2>
            <p>
              El acceso al servicio se realiza mediante enlaces mágicos enviados a tu correo electrónico. Eres responsable de mantener la confidencialidad de tu acceso.
            </p>
            <p>
              CleanMail opera bajo un modelo de consumo por créditos prepagados. Un (1) crédito equivale a la validación de un (1) correo electrónico. Los créditos comprados no expiran y permanecen activos en tu cuenta hasta que sean utilizados.
            </p>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">5. Limitación de Responsabilidad</h2>
            <p>
              CleanMail realiza verificaciones de sintaxis, DNS y conexiones SMTP en tiempo real para evaluar la validez de los correos electrónicos. Sin embargo, debido a configuraciones de servidores externos, políticas de privacidad cambiantes de los proveedores de correo y bloqueos temporales, no podemos garantizar un 100% de precisión matemática en todos los resultados.
            </p>
            <p>
              El Servicio se proporciona "tal cual" y "según disponibilidad". We Are Samod no será responsable de ningún daño indirecto, incidental o especial que resulte del uso o de la imposibilidad de usar el servicio.
            </p>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">6. Modificaciones de los Términos</h2>
            <p>
              Nos reservamos el derecho de modificar estos términos en cualquier momento. Notificaremos cualquier cambio sustancial publicando los nuevos términos en esta página. El uso continuado del Servicio después de dichos cambios constituye tu aceptación de los nuevos Términos de Servicio.
            </p>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">7. Ley Aplicable y Jurisdicción</h2>
            <p>
              Estos términos se regirán e interpretarán de conformidad con las leyes de la República de Chile. Cualquier disputa que surja en relación con estos términos estará sujeta a la jurisdicción exclusiva de los tribunales competentes de Santiago de Chile.
            </p>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">8. Contacto</h2>
            <p>
              Para cualquier consulta sobre estos Términos de Servicio, puedes contactarnos en:
            </p>
            <p class="font-semibold text-brand-text">
              We Are Samod<br />
              Email: contacto@wearesamod.com<br />
              Sitio Web: https://wearesamod.com
            </p>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
