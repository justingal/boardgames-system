<template>
  <div class="min-h-screen bg-gray-50 py-10">
    <div v-if="event" class="max-w-5xl mx-auto px-4 sm:px-6">
      <!-- Renginio antraštė ir pagrindinė informacija -->
      <div class="bg-white rounded-xl overflow-hidden shadow-lg mb-8 relative">
        <!-- Renginio viršutinė juosta su statusu -->
        <div class="h-3 bg-gradient-to-r from-indigo-500 to-blue-600"></div>

        <div class="p-6 sm:p-8">
          <div class="flex flex-col md:flex-row md:justify-between md:items-start gap-4">
            <!-- Kairė pusė: pavadinimas ir detalės -->
            <div class="flex-1">
              <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ event.title }}</h1>

              <div class="flex items-center flex-wrap gap-3 mb-6">
                <!-- "First player is organizer" badge -->
                <div v-if="event.first_player_is_organizer"
                     class="inline-flex items-center bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                  <svg class="h-3.5 w-3.5 mr-1.5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>
                  Pirmas prisijungęs žaidėjas tampa organizatoriumi
                </div>
                <div class="inline-flex items-center gap-1 text-sm text-gray-600 px-3 py-1 rounded-full bg-gray-100">
                  <span>{{ privacyLabels[event.visibility] }}</span>
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4 text-sm">
                <div class="flex items-start">
                  <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-gray-500 mb-1">Adresas</p>
                    <p class="font-medium text-gray-900">{{ event.address }}</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-gray-500 mb-1">Stalo dydis</p>
                    <p class="font-medium text-gray-900">{{ tableSizeLabels[event.table_size] }}</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-gray-500 mb-1">Pradžia</p>
                    <p class="font-medium text-gray-900">{{ formatDateTime(event.start_time) }}</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-gray-500 mb-1">Pabaiga</p>
                    <p class="font-medium text-gray-900">{{ formatDateTime(event.end_time) }}</p>
                  </div>
                </div>

                <div class="flex items-start md:col-span-2">
                  <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-gray-500 mb-1">Organizatoriai</p>
                    <p class="font-medium text-gray-900">
                      <span v-if="event.organizers && event.organizers.length > 0">
                        {{ event.organizers.map(org => org.username).join(', ') }}
                      </span>
                      <span v-else>{{ event.created_by }}</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Dešinė pusė: veiksmai -->
            <div class="flex flex-col gap-3 md:w-1/4">
              <!-- Join/Leave Event Button -->
              <button
                v-if="!userIsParticipant && !userIsOrganizer"
                @click="joinEvent"
                :disabled="joiningEvent"
                class="flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 shadow-sm transition disabled:opacity-50"
              >
                <svg v-if="!joiningEvent" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                <svg v-else class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ joiningEvent ? 'Prisijungiama...' : (event.first_player_is_organizer && (!event.players || event.players.length === 0) ? 'Tapti organizatoriumi' : 'Prisijungti') }}
              </button>

              <button
                v-if="userIsParticipant && !userIsOrganizer"
                @click="leaveEvent"
                :disabled="leavingEvent"
                class="flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 shadow-sm transition disabled:opacity-50"
              >
                <svg v-if="!leavingEvent" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                <svg v-else class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ leavingEvent ? 'Išeinama...' : 'Išeiti' }}
              </button>

              <button
                v-if="userIsOrganizer"
                @click="showEditModal = true"
                class="flex items-center justify-center gap-2 px-4 py-2.5 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition shadow-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
                Redaguoti renginį
              </button>

              <button
                v-if="userIsOrgCreator"
                @click="deleteEvent"
                class="flex items-center justify-center gap-2 px-4 py-2.5 bg-white border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition shadow-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Ištrinti renginį
              </button>
            </div>
          </div>

          <!-- Aprašymas -->
          <div class="mt-8 p-4 bg-gray-50 rounded-lg text-sm leading-relaxed border border-gray-200">
            <h3 class="font-medium text-gray-900 mb-2">Aprašymas:</h3>
            <p class="text-gray-700 whitespace-pre-line">{{ event.description }}</p>
          </div>

          <!-- Pranešimai -->
          <div v-if="message" class="mt-6 p-4 rounded-lg border" :class="messageClass">
            {{ message }}
          </div>
        </div>
      </div>

      <!-- Dalyviai ir žaidimai -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Dalyvių sąrašas -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="bg-gradient-to-r from-indigo-500 to-blue-600 px-6 py-4 flex justify-between items-center">
              <h2 class="text-lg font-semibold text-white flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                Dalyviai ({{ event.players?.length || 0 }})
              </h2>

              <!-- Invite Participants Button -->
              <button
                v-if="userIsOrganizer"
                @click="showInviteModal = true"
                class="px-3 py-1.5 bg-white/20 text-white text-sm rounded-md hover:bg-white/30 transition shadow-sm flex items-center gap-1"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Kviesti
              </button>
            </div>

            <!-- Join Requests - PERKELTAS Į VIRŠŲ -->
            <div v-if="userIsOrganizer && joinRequests && joinRequests.length > 0" class="border-b border-gray-200 bg-yellow-50">
              <div class="p-4">
                <h3 class="font-semibold mb-3 text-gray-800 flex items-center">
                  <svg class="w-5 h-5 text-yellow-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 3 1.732 3z" />
                  </svg>
                  Laukiantys prisijungimo prašymai ({{ joinRequests.length }})
                </h3>
                <div class="space-y-2">
                  <div v-for="request in joinRequests" :key="request.id" class="bg-white rounded-lg shadow-sm p-3">
                    <div class="flex items-center mb-3">
                      <div class="w-10 h-10 bg-yellow-100 text-yellow-700 rounded-full flex items-center justify-center font-semibold mr-3 flex-shrink-0">
                        {{ request.user_username?.charAt(0)?.toUpperCase() || '?' }}
                      </div>
                      <div class="min-w-0 flex-1">
                        <p class="font-medium text-gray-800 truncate">{{ request.user_username || 'Nežinomas vartotojas' }}</p>
                        <p class="text-sm text-gray-500 truncate">{{ request.user_email || '' }}</p>
                      </div>
                    </div>
                    <div class="flex gap-2">
                      <button
                        @click="approveRequest(request.id)"
                        class="flex-1 px-3 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 transition font-medium flex items-center justify-center gap-1"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                        Priimti
                      </button>
                      <button
                        @click="rejectRequest(request.id)"
                        class="flex-1 px-3 py-2 bg-red-600 text-white text-sm rounded-md hover:bg-red-700 transition font-medium flex items-center justify-center gap-1"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                        Atmesti
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Participants List -->
            <div v-if="event.players && event.players.length > 0" class="divide-y divide-gray-200">
              <div v-for="player in event.players" :key="player.id" class="p-4 hover:bg-gray-50 transition">
                <div class="flex items-center justify-between">
                  <div class="flex items-center flex-1 min-w-0">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-blue-600 flex items-center justify-center text-white font-bold mr-3 flex-shrink-0 shadow-sm">
                      {{ player.username.charAt(0).toUpperCase() }}
                    </div>
                    <div class="min-w-0 flex-1">
                      <p class="font-medium text-gray-900 truncate">{{ player.username }}</p>
                      <div class="flex items-center gap-2">
                <span v-if="isOrganizer(player.id)" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                  <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  Organizatorius
                </span>
                        <span v-if="player.id === user?.id" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                  Tu
                </span>
                      </div>
                    </div>
                  </div>

                  <!-- Veiksmai -->
                  <div v-if="userIsOrganizer && player.id !== user?.id" class="flex items-center gap-2 ml-3">
                    <button
                      v-if="!isOrganizer(player.id)"
                      @click="makeOrganizer(player.id)"
                      class="px-3 py-1.5 bg-indigo-50 text-indigo-700 text-sm rounded-md hover:bg-indigo-100 transition font-medium"
                      title="Suteikti organizatoriaus teises"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </button>
                    <button
                      v-else-if="canRemoveOrganizerStatus(player.id)"
                      @click="removeOrganizer(player.id)"
                      class="px-3 py-1.5 bg-orange-50 text-orange-700 text-sm rounded-md hover:bg-orange-100 transition font-medium"
                      title="Atimti organizatoriaus teises"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </button>
                    <button
                      v-if="canKickPlayer(player.id)"
                      @click="kickPlayer(player.id)"
                      class="px-3 py-1.5 bg-red-50 text-red-700 text-sm rounded-md hover:bg-red-100 transition font-medium"
                      title="Išmesti iš renginio"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7a4 4 0 11-8 0 4 4 0 018 0zM9 14a6 6 0 00-6 6v1h18v-1a6 6 0 00-6-6v-1m-3 1a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-else class="p-12 text-center">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">Dar nėra dalyvių</h3>
              <p class="text-gray-500 mb-6">Būkite pirmas prisijungęs prie šio renginio!</p>
              <button
                v-if="!userIsParticipant && !userIsOrganizer"
                @click="joinEvent"
                :disabled="joiningEvent"
                class="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-lg hover:from-indigo-700 hover:to-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-sm font-medium"
              >
                <svg v-if="!joiningEvent" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v-3a3 3 0 00-3-3H5a3 3 0 00-3 3v6m3 0h12m-3 0l3 3m-3-3l3-3m-12 3l-3 3m3-3l-3-3" />
                </svg>
                <svg v-else class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ joiningEvent ? 'Prisijungiama...' : 'Prisijungti prie renginio' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Participant Invitation Modal -->
        <div v-if="showInviteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div class="bg-white rounded-xl shadow-xl max-w-md w-full max-h-[90vh] flex flex-col">
            <!-- Modal Header -->
            <div class="flex justify-between items-center p-6 border-b border-gray-200">
              <h3 class="text-xl font-semibold text-gray-900">Kviesti dalyvius</h3>
              <button
                @click="closeInviteModal"
                class="text-gray-400 hover:text-gray-600 transition p-1 rounded-lg hover:bg-gray-100"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Modal Body -->
            <div class="p-6 flex-1 overflow-hidden flex flex-col">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Ieškoti vartotojo
                </label>
                <div class="relative">
                  <input
                    v-model="searchQuery"
                    @input="searchUsers"
                    type="text"
                    placeholder="Įveskite vardą arba el. paštą..."
                    class="w-full px-4 py-2.5 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                  />
                  <svg class="absolute left-3 top-3 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>

              <!-- Search results -->
              <div class="flex-1 overflow-y-auto">
                <div v-if="searchResults.length > 0" class="space-y-2">
                  <h4 class="text-sm font-medium text-gray-700 mb-3">Rasti vartotojai:</h4>
                  <div
                    v-for="searchUser in searchResults"
                    :key="searchUser.id"
                    class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
                  >
                    <div class="flex items-center flex-1 min-w-0">
                      <div class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-full flex items-center justify-center font-semibold mr-3 flex-shrink-0">
                        {{ searchUser.username.charAt(0).toUpperCase() }}
                      </div>
                      <div class="min-w-0 flex-1">
                        <p class="font-medium text-gray-900 truncate">{{ searchUser.username }}</p>
                        <p class="text-sm text-gray-500 truncate">{{ searchUser.email }}</p>
                      </div>
                    </div>
                    <button
                      @click="inviteUser(searchUser.id)"
                      :disabled="invitingUsers.includes(searchUser.id)"
                      class="ml-3 px-4 py-2 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition font-medium flex-shrink-0"
                    >
                      {{ invitingUsers.includes(searchUser.id) ? 'Siunčiama...' : 'Kviesti' }}
                    </button>
                  </div>
                </div>

                <div v-else-if="searchQuery && searchQuery.length >= 2" class="text-center py-8">
                  <div class="inline-flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mb-3">
                    <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <p class="text-gray-500">Vartotojų nerasta</p>
                  <p class="text-sm text-gray-400 mt-1">Pabandykite kitą paieškos užklausą</p>
                </div>

                <div v-else class="text-center py-8">
                  <div class="inline-flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-full mb-3">
                    <svg class="w-8 h-8 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                  <p class="text-gray-600 font-medium">Pradėkite rašyti, kad rastumėte vartotojus</p>
                  <p class="text-sm text-gray-400 mt-1">Įveskite bent 2 simbolius</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Žaidimų sąrašas -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="bg-gradient-to-r from-indigo-500 to-blue-600 px-6 py-4 flex justify-between items-center">
              <h2 class="text-lg font-semibold text-white flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Žaidimai ({{ visibleGames.length }}/{{ allGames.length }})
              </h2>

              <div class="flex items-center gap-2">
                <button
                  @click="showImportModal = true"
                  class="px-3 py-1.5 bg-green-500 text-white text-sm rounded-md hover:bg-green-600 transition shadow-sm flex items-center gap-1"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                  Importuoti
                </button>

                <button
                  @click="showVoteModal = true"
                  class="px-3 py-1.5 bg-blue-500 text-white text-sm rounded-md hover:bg-blue-800 transition shadow-sm flex items-center gap-1"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Balsuoti
                </button>
              </div>
            </div>

            <div v-if="visibleGames.length > 0" class="p-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div v-for="(item, index) in visibleGames" :key="item.game.id"
                     class="flex gap-3 border rounded-lg p-3 bg-gray-50 hover:bg-gray-100 transition">
                  <div class="w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-xs flex items-center justify-center flex-shrink-0">
                    {{ index + 1 }}
                  </div>
                  <img :src="item.game.thumbnail_url" class="w-14 h-14 object-cover rounded-md" />
                  <div class="overflow-hidden">
                    <p class="font-medium text-sm truncate">
                      {{ item.game.title }}
                    </p>

                    <!-- 🏆 Vieta (rank) -->
                    <span class="text-xs text-gray-500">🗳️ Balsų suma: {{ item.total_score ?? '–' }}</span>

                    <!-- 🗳️ Balsų kiekis -->
                    <p v-if="item.vote_count > 0" class="text-xs text-gray-500">
                      🗳️ Balsų sk.: {{ item.vote_count }}
                    </p>

                    <p class="text-xs text-gray-600">
                      {{ item.game.min_players }}–{{ item.game.max_players }} žaidėjai • {{ item.game.playtime_minutes }} min
                    </p>
                  </div>
                </div>
              </div>

              <div v-if="visibleGames.length < allGames.length" class="mt-4 text-center">
                <button @click="showMoreGames" class="px-4 py-2 bg-gray-100 text-gray-600 rounded-md hover:bg-gray-200 transition">
                  Rodyti daugiau žaidimų
                </button>
              </div>
            </div>

            <div v-else class="p-6 text-center text-gray-500">
              Nėra pasirinktų žaidimų. Importuokite žaidimus arba balsuokite už juos.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loaderis kol event dar neatėjo -->
    <div v-else class="flex justify-center items-center h-screen">
      <div class="text-center">
        <svg class="animate-spin h-12 w-12 mx-auto text-indigo-600 mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-lg font-medium text-gray-700">Kraunama renginio informacija...</p>
      </div>
    </div>

    <!-- Modalai -->
    <ImportGamesModal
      :visible="showImportModal"
      @close="showImportModal = false"
      @imported="handleGamesImported"
    />
    <EventVoteModal
      ref="voteModalRef"
      :visible="showVoteModal"
      @close="showVoteModal = false"
      @voted="fetchGames"
    />

    <EditEventModal
      :visible="showEditModal"
      :eventData="event"
      @close="showEditModal = false"
      @updated="handleEventUpdated"
    />
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, computed, watch, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/api/axios'
import EditEventModal from '@/components/EditEventModal.vue'
import ImportGamesModal from '@/components/ImportGamesModal.vue'
import EventVoteModal from "@/components/EventVoteModal.vue";

const showVoteModal = ref(false)
const showImportModal = ref(false)
const router = useRouter()
const token = localStorage.getItem('access')
const voteModalRef = ref()

const route = useRoute()
const event = ref<any>(null)
const message = ref('')
const messageClass = ref('bg-green-100 text-green-800')
const user = ref<any>(null)
const joinRequests = ref<any[]>([])

// UI state
const showInviteModal = ref(false)
const joiningEvent = ref(false)
const leavingEvent = ref(false)

// Search functionality
const searchQuery = ref('')
const searchResults = ref([])
const invitingUsers = ref<number[]>([])

const tableSizeLabels = {
  S: 'Mažas',
  M: 'Vidutinis',
  L: 'Didelis',
  XL: 'Labai didelis',
}

const privacyLabels = {
  public: '🔓 Viešas',
  protected: '🔐 Apsaugotas',
  private: '🚫 Privatus',
}

// Computed properties
const userIsParticipant = computed(() => {
  if (!event.value || !user.value) return false
  return event.value.players?.some((player: any) => player.id === user.value.id) || false
})

const userIsOrganizer = computed(() => {
  if (!event.value || !user.value) return false

  const isInOrganizersList = event.value.organizers?.some((org: any) => org.id === user.value.id) || false
  const isCreator = event.value.created_by === user.value.username

  return isInOrganizersList || isCreator
})

const userIsOrgCreator = computed(() => {
  return event.value?.organization_creator === user.value?.username
})

// Functions
const handleGamesImported = async () => {
  await fetchGames()
  await fetchEvent()
}

const formatDateTime = (datetimeStr: string) => {
  if (!datetimeStr) return '';

  const date = new Date(datetimeStr);
  const options: Intl.DateTimeFormatOptions = {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: 'UTC'
  };

  return date.toLocaleString('lt-LT', options);
}

const fetchEvent = async () => {
  try {
    const res = await axios.get(`/events/${route.params.id}/`)
    event.value = res.data
    console.log('Event loaded:', res.data)
  } catch (err) {
    console.error('Nepavyko gauti renginio:', err)
    message.value = '❌ Klaida gaunant renginio informaciją.'
    messageClass.value = 'bg-red-100 text-red-800'
  }
}

const fetchUser = async () => {
  try {
    const res = await axios.get('/users/me/')
    user.value = res.data
    console.log('User loaded:', res.data)
  } catch (err) {
    console.error('Nepavyko gauti vartotojo informacijos:', err)
  }
}

const fetchJoinRequests = async () => {
  console.log('fetchJoinRequests called!')

  if (!event.value || !user.value) {
    console.log('No event or user yet:', { event: event.value, user: user.value })
    return
  }

  console.log('Checking if user is organizer:', userIsOrganizer.value)

  if (!userIsOrganizer.value) {
    console.log('User is not organizer, skipping join requests fetch')
    return
  }

  try {
    console.log('Fetching join requests for event:', route.params.id)
    const res = await axios.get(`/events/${route.params.id}/join_requests/`)
    console.log('Join requests received:', res.data)
    joinRequests.value = res.data
  } catch (err) {
    console.error('Nepavyko gauti prisijungimo prašymų:', err)
  }
}

// Watch for when both event and user are loaded, then fetch join requests if user is organizer
watchEffect(() => {
  if (event.value && user.value && userIsOrganizer.value) {
    console.log('Conditions met, fetching join requests...')
    fetchJoinRequests()
  }
})

// Join/Leave event functionality
const joinEvent = async () => {
  joiningEvent.value = true
  try {
    const res = await axios.post(`/events/${route.params.id}/join/`)
    message.value = res.data.detail || '✅ Sėkmingai prisijungėte prie renginio!'
    messageClass.value = 'bg-green-100 text-green-800'
    await fetchEvent()
  } catch (err: any) {
    console.error('Klaida prisijungiant prie renginio:', err)
    if (err.response?.status === 400) {
      message.value = err.response.data.detail || '❌ Negalite prisijungti prie šio renginio.'
    } else {
      message.value = '❌ Klaida prisijungiant prie renginio.'
    }
    messageClass.value = 'bg-red-100 text-red-800'
  } finally {
    joiningEvent.value = false
  }
}

const leaveEvent = async () => {
  if (!confirm('Ar tikrai norite išeiti iš šio renginio?')) return

  leavingEvent.value = true
  try {
    const res = await axios.post(`/events/${route.params.id}/leave/`)
    message.value = res.data.detail || '✅ Sėkmingai išėjote iš renginio.'
    messageClass.value = 'bg-green-100 text-green-800'
    await fetchEvent()
  } catch (err) {
    console.error('Klaida išeinant iš renginio:', err)
    message.value = '❌ Klaida išeinant iš renginio.'
    messageClass.value = 'bg-red-100 text-red-800'
  } finally {
    leavingEvent.value = false
  }
}

// User search and invitation
const searchUsers = async () => {
  if (searchQuery.value.length < 2) {
    searchResults.value = []
    return
  }

  try {
    const res = await axios.get('/users/search/', {
      params: { q: searchQuery.value }
    })
    // Filter out users who are already participants
    const participantIds = event.value.players?.map((player: any) => player.id) || []
    searchResults.value = res.data.filter((user: any) => !participantIds.includes(user.id))
  } catch (error) {
    console.error('Error searching users:', error)
    searchResults.value = []
  }
}

const inviteUser = async (userId: number) => {
  if (invitingUsers.value.includes(userId)) return

  invitingUsers.value.push(userId)

  try {
    await axios.post(`/events/${route.params.id}/invite/`, {
      user_id: userId
    })

    message.value = '✅ Kvietimas sėkmingai išsiųstas!'
    messageClass.value = 'bg-green-100 text-green-800'

    // Remove user from search results after successful invitation
    searchResults.value = searchResults.value.filter((user: any) => user.id !== userId)
  } catch (error) {
    console.error('Error inviting user:', error)
    message.value = '❌ Nepavyko išsiųsti kvietimo. Bandykite dar kartą.'
    messageClass.value = 'bg-red-100 text-red-800'
  } finally {
    invitingUsers.value = invitingUsers.value.filter(id => id !== userId)
  }
}

const closeInviteModal = () => {
  showInviteModal.value = false
  searchQuery.value = ''
  searchResults.value = []
  invitingUsers.value = []
}

const approveRequest = async (requestId: number) => {
  try {
    const res = await axios.post(`/events/${route.params.id}/approve_request/`, {
      request_id: requestId
    })

    message.value = res.data.detail || '✅ Naudotojas patvirtintas.'
    messageClass.value = 'bg-green-100 text-green-800'
    await fetchEvent()
    await fetchJoinRequests()
  } catch (err) {
    console.error('Klaida tvirtinant naudotoją:', err)
    message.value = '❌ Klaida tvirtinant prisijungimą.'
    messageClass.value = 'bg-red-100 text-red-800'
  }
}

const rejectRequest = async (requestId: number) => {
  try {
    const res = await axios.post(`/events/${route.params.id}/reject_request/`, {
      request_id: requestId
    })

    message.value = res.data.detail || '✅ Prašymas atmestas.'
    messageClass.value = 'bg-green-100 text-green-800'
    await fetchJoinRequests()
  } catch (err) {
    console.error('Klaida atmetant prašymą:', err)
    message.value = '❌ Klaida atmetant prašymą.'
    messageClass.value = 'bg-red-100 text-red-800'
  }
}

// Check if a specific player is an organizer
const isOrganizer = (playerId: number) => {
  if (!event.value || !event.value.organizers) return false
  return event.value.organizers.some((org: any) => org.id === playerId)
}

// Check if current user can remove organizer status from a player
const canRemoveOrganizerStatus = (playerId: number) => {
  if (!event.value || !user.value) return false

  // You can't remove yourself if you're the creator
  if (playerId === user.value.id && event.value.created_by === user.value.username) {
    return false
  }

  return true
}

// Check if current user can kick a player
const canKickPlayer = (playerId: number) => {
  if (!event.value || !user.value) return false

  // Can't kick organizers
  if (isOrganizer(playerId)) {
    return false
  }

  return true
}

const makeOrganizer = async (userId: number) => {
  try {
    const res = await axios.post(`/events/${route.params.id}/make-organizer/`, { user_id: userId })
    message.value = res.data.message || '✅ Organizatoriaus teisės suteiktos.'
    messageClass.value = 'bg-green-100 text-green-800'
    await fetchEvent()
  } catch (err) {
    console.error('Klaida suteikiant organizatoriaus teises:', err)
    message.value = '❌ Klaida suteikiant organizatoriaus teises.'
    messageClass.value = 'bg-red-100 text-red-800'
  }
}

const deleteEvent = async () => {
  if (!confirm('Ar tikrai nori ištrinti šį renginį?')) return
  try {
    await axios.delete(`/events/${event.value.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('✅ Renginys ištrintas.')
    router.push('/events')
  } catch (error) {
    console.error('Nepavyko ištrinti renginio:', error)
    alert('❌ Klaida trinant renginį.')
  }
}

const removeOrganizer = async (userId: number) => {
  try {
    const res = await axios.post(`/events/${route.params.id}/remove-organizer/`, { user_id: userId })
    message.value = res.data.message || '✅ Organizatoriaus teisės pašalintos.'
    messageClass.value = 'bg-green-100 text-green-800'
    await fetchEvent()
  } catch (err) {
    console.error('Klaida šalinant organizatoriaus teises:', err)
    message.value = '❌ Klaida šalinant organizatoriaus teises.'
    messageClass.value = 'bg-red-100 text-red-800'
  }
}

const kickPlayer = async (userId: number) => {
  if (!confirm('Ar tikrai norite išmesti šį žaidėją?')) return

  try {
    const res = await axios.post(`/events/${route.params.id}/kick-player/`, { user_id: userId })
    message.value = res.data.message || '✅ Žaidėjas išmestas.'
    messageClass.value = 'bg-green-100 text-green-800'
    await fetchEvent()
  } catch (err) {
    console.error('Klaida metant žaidėją lauk:', err)
    message.value = '❌ Klaida metant žaidėją lauk.'
    messageClass.value = 'bg-red-100 text-red-800'
  }
}

const showEditModal = ref(false)

const handleEventUpdated = async () => {
  await fetchEvent()
  message.value = '✅ Renginys atnaujintas!'
  messageClass.value = 'bg-green-100 text-green-800'
}

const allGames = ref<any[]>([])
const visibleGames = ref<any[]>([])
const gamesToShow = ref(10)

const fetchGames = async () => {
  try {
    const res = await axios.get(`/events/${route.params.id}/available-games/`)
    allGames.value = res.data
    visibleGames.value = allGames.value.slice(0, gamesToShow.value)
  } catch (err) {
    console.error('Nepavyko gauti žaidimų:', err)
  }
}

const showMoreGames = () => {
  gamesToShow.value += 10
  visibleGames.value = allGames.value.slice(0, gamesToShow.value)
}

// Mount hook - load initial data
onMounted(async () => {
  try {
    // Load user and event data in parallel
    await Promise.all([
      fetchUser(),
      fetchEvent()
    ])

    console.log('Initial data loaded successfully')

    // Load games after event is loaded
    fetchGames()

    // Join requests will be loaded automatically by watchEffect when conditions are met
  } catch (error) {
    console.error('Error loading initial data:', error)
  }
})
</script>
