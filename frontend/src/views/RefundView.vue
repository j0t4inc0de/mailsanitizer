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
          Política de Reembolso
        </h1>
        <p class="text-brand-muted text-sm mb-8">
          Última actualización: 04 de junio, 2026
        </p>

        <div class="space-y-6 text-brand-muted text-sm leading-relaxed">
          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">1. Modelo de Consumo por Créditos</h2>
            <p>
              CleanMail by Samod funciona bajo un modelo prepagado de créditos (Pay-as-you-go). No existen cobros recurrentes mensuales, suscripciones automáticas ni cuotas de mantenimiento. Compras un paquete de créditos específico y consumes exactamente un (1) crédito por cada correo electrónico validado.
            </p>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">2. Reembolsos para Créditos No Utilizados</h2>
            <p>
              Ofrecemos una garantía de reembolso de 14 días para los créditos adquiridos que **no hayan sido utilizados**. Si compraste un paquete de créditos por error o decidiste no usarlos, puedes solicitar un reembolso completo del 100% de tu compra bajo las siguientes condiciones:
            </p>
            <ul class="list-disc pl-5 space-y-1">
              <li>La solicitud debe realizarse dentro de los **14 días naturales** posteriores a la fecha de compra.</li>
              <li>El saldo total de créditos adquiridos en esa transacción específica debe estar **intacto** (no se debe haber iniciado ningún proceso de validación masiva ni de prueba posterior a la compra).</li>
            </ul>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">3. Reembolsos para Créditos Consumidos</h2>
            <p>
              Debido a la naturaleza del servicio de software (donde los recursos de red, cómputo DNS y conexiones de correo se consumen instantáneamente al subir una lista), **no se ofrecen reembolsos sobre créditos que ya hayan sido utilizados para validar correos**.
            </p>
            <p>
              Antes de validar una lista grande, te recomendamos utilizar los **50 créditos iniciales gratuitos** para probar la calidad de nuestra verificación de manera libre y sin compromiso.
            </p>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">4. Fallos Técnicos o Errores de Procesamiento</h2>
            <p>
              Si durante un análisis masivo ocurre un fallo técnico atribuible a nuestros servidores (por ejemplo, caída del servicio, fallo de cola o corrupción de archivo) y los créditos se consumieron sin entregarte el reporte limpio correspondiente:
            </p>
            <p>
              Por favor, contáctanos inmediatamente a soporte y realizaremos una de las siguientes acciones tras comprobar el error en los logs:
            </p>
            <ul class="list-disc pl-5 space-y-1">
              <li>Reversión/devolución completa de los créditos consumidos a tu cuenta para que puedas repetir la validación.</li>
              <li>Reembolso monetario equivalente de la proporción de créditos afectados por el fallo si el sistema no puede procesar el archivo.</li>
            </ul>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">5. Cómo Solicitar un Reembolso</h2>
            <p>
              Para iniciar una solicitud de reembolso, envía un correo electrónico a nuestro equipo de soporte con la siguiente información:
            </p>
            <ul class="list-disc pl-5 space-y-1">
              <li>El correo electrónico asociado a tu cuenta de CleanMail.</li>
              <li>El número de recibo o confirmación de la compra (provisto por Paddle).</li>
              <li>El paquete de créditos que deseas reembolsar.</li>
            </ul>
            <p class="mt-2 font-semibold text-brand-text">
              Contacto de Soporte:<br />
              Email: contacto@wearesamod.com
            </p>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
