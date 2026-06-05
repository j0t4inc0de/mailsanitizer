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
          Política de Privacidad
        </h1>
        <p class="text-brand-muted text-sm mb-8">
          Última actualización: 04 de junio, 2026
        </p>

        <div class="space-y-6 text-brand-muted text-sm leading-relaxed">
          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">1. Introducción</h2>
            <p>
              En CleanMail by Samod (en adelante, "nosotros" o "la Plataforma"), valoramos enormemente la privacidad de nuestros usuarios y de los titulares de las direcciones de correo electrónico que procesamos. Esta Política de Privacidad describe cómo recopilamos, utilizamos, almacenamos y protegemos la información personal en cumplimiento con las normativas internacionales de protección de datos (como GDPR y normativas de privacidad locales).
            </p>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">2. Información que Recopilamos</h2>
            <p>
              Para prestar nuestros servicios, recopilamos las siguientes categorías de datos:
            </p>
            <ul class="list-disc pl-5 space-y-1">
              <li>
                <strong>Información de tu Cuenta:</strong> Tu dirección de correo electrónico, nombre (opcional), historial de transacciones de créditos y registros de acceso.
              </li>
              <li>
                <strong>Listas de Correo que Subes:</strong> Los archivos CSV que cargas en nuestra plataforma contienen direcciones de correo electrónico de terceros para su respectiva validación.
              </li>
              <li>
                <strong>Datos de Uso Técnico:</strong> Direcciones IP de origen (utilizadas únicamente para mitigación de fraudes y límites de uso del API público), tipo de navegador y datos de telemetría de interacción con la aplicación.
              </li>
            </ul>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">3. Procesamiento y Seguridad de las Listas Subidas</h2>
            <p>
              Garantizamos el más alto nivel de confidencialidad en el procesamiento de tus listas de correos:
            </p>
            <ul class="list-disc pl-5 space-y-1">
              <li>
                <strong>No almacenamiento definitivo:</strong> Las direcciones de correo electrónico que subes se procesan en memoria y bases de datos seguras de forma temporal únicamente para generar los reportes de validación.
              </li>
              <li>
                <strong>No comercialización:</strong> Bajo ninguna circunstancia vendemos, alquilamos, compartimos o utilizamos las direcciones de correo electrónico que subes para campañas de marketing propias o de terceros.
              </li>
              <li>
                <strong>Depuración automática (Purgado):</strong> Todos los archivos de listas subidas, registros de validaciones intermedias y archivos de resultados descargables se eliminan de forma permanente y definitiva de nuestros servidores después de **30 días corridos** de haber finalizado el proceso de validación.
              </li>
            </ul>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">4. Uso de la Información de la Cuenta</h2>
            <p>
              La información personal de tu cuenta se utiliza exclusivamente para:
            </p>
            <ul class="list-disc pl-5 space-y-1">
              <li>Autenticar y administrar tu cuenta mediante el envío de enlaces mágicos de inicio de sesión.</li>
              <li>Proporcionar soporte técnico y responder a tus solicitudes.</li>
              <li>Procesar las compras de créditos y mantener tu historial de facturación.</li>
              <li>Enviar notificaciones operativas importantes (ej. finalización de un análisis masivo).</li>
            </ul>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">5. Transferencias a Terceros e Integraciones</h2>
            <p>
              No vendemos ni transferimos tu información personal a terceros, excepto a los proveedores de servicios que nos ayudan a operar la plataforma de manera segura, tales como:
            </p>
            <ul class="list-disc pl-5 space-y-1">
              <li><strong>Pasarelas de Pago:</strong> Procesadores de pago como Paddle, que administran la facturación segura de créditos.</li>
              <li><strong>Infraestructura en la nube:</strong> Proveedores de servidores seguros VPS y base de datos donde se aloja de forma encriptada la plataforma.</li>
            </ul>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">6. Tus Derechos (Acceso, Rectificación y Supresión)</h2>
            <p>
              Como usuario de nuestra plataforma, tienes el derecho de solicitar el acceso a la información personal que poseemos de ti, solicitar su corrección si es inexacta, o solicitar la eliminación total y permanente de tu cuenta y todos los datos asociados enviando un correo a soporte.
            </p>
          </section>

          <section class="space-y-2">
            <h2 class="font-outfit text-xl font-bold text-brand-text">7. Contacto</h2>
            <p>
              Si tienes preguntas sobre esta Política de Privacidad o deseas ejercer tus derechos de protección de datos, puedes contactarnos en:
            </p>
            <p class="font-semibold text-brand-text">
              We Are Samod<br />
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
