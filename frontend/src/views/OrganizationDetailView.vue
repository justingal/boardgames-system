<template>
  <div class="bg-gray-50 min-h-screen py-8">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div v-if="!organization" class="flex justify-center items-center py-16">
        <div class="text-center">
          <svg class="animate-spin h-12 w-12 mx-auto text-indigo-600 mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="text-lg font-medium text-gray-700">Kraunama organizacijos informacija...</p>
        </div>
      </div>

      <div v-else>
        <!-- Organizacijos informacija -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden mb-8">
          <div class="h-3 bg-gradient-to-r from-indigo-500 to-blue-600"></div>
          <div class="p-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
              <h1 class="text-3xl font-bold text-gray-800">{{ organization.name }}</h1>
              <button
                v-if="userIsCreator"
                @click="showEditModal = true"
                class="px-4 py-2 bg-gradient-to-r from-amber-500 to-amber-600 text-white rounded-lg hover:from-amber-600 hover:to-amber-700 shadow-sm transition flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
                Redaguoti
              </button>
            </div>

            <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-6">
              <p class="text-gray-700">{{ organization.description }}</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="flex items-start">
                <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div>
                  <p class="text-gray-500 text-sm">Miestas</p>
                  <p class="font-medium text-gray-900 capitalize">{{ organization.city }}</p>
                </div>
              </div>

              <div class="flex items-start">
                <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div>
                  <p class="text-gray-500 text-sm">Sukūrė</p>
                  <p class="font-medium text-gray-900">{{ organization.created_by }}</p>
                </div>
              </div>

              <div class="flex items-start">
                <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <div>
                  <p class="text-gray-500 text-sm">Narių skaičius</p>
                  <p class="font-medium text-gray-900">{{ organization.members.length }}</p>
                </div>
              </div>

              <div class="flex items-start">
                <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </div>
                <div>
                  <p class="text-gray-500 text-sm">Viešumo tipas</p>
                  <p class="font-medium text-gray-900">{{ privacyLabels[organization.privacy] }}</p>
                </div>
              </div>

              <div class="flex items-start md:col-span-2">
                <div class="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex-shrink-0">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                </div>
                <div>
                  <p class="text-gray-500 text-sm">Grupė</p>
                  <p class="font-medium text-gray-900">
                    <span v-if="organization.category">{{ getCategoryName(organization.category) }}</span>
                    <span v-else-if="organization.categories && organization.categories.length > 0">
                      {{ organization.categories.map(cat => cat.name).join(', ') }}
                    </span>
                    <span v-else class="italic text-gray-400">Nenurodyta</span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Organizacijos renginiai -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden mb-10">
          <div class="h-3 bg-gradient-to-r from-green-500 to-green-600"></div>
          <div class="p-6">
            <div class="flex items-center mb-6">
              <div class="w-10 h-10 rounded-full bg-green-100 text-green-600 flex items-center justify-center mr-3">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h2 class="text-2xl font-bold text-green-700">Renginiai</h2>
              <span class="ml-3 bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                {{ organization.events.length }} renginiai
              </span>
            </div>

            <div v-if="organization.events.length === 0" class="bg-gray-50 p-10 rounded-lg border border-gray-200 text-center">
              <div class="flex flex-col items-center">
                <svg class="w-12 h-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="text-gray-500 text-lg font-medium">Šiuo metu nėra renginių</p>
                <p class="text-gray-400 mt-1">Greitai tikėkimės naujų renginių</p>
              </div>
            </div>

            <div v-else class="space-y-5">
              <div
                v-for="event in organization.events"
                :key="event.id"
                class="border rounded-lg overflow-hidden bg-white shadow-sm hover:shadow-md transition"
              >
                <div class="h-1.5 bg-gradient-to-r from-indigo-500 to-blue-600"></div>

                <div class="p-5">
                  <h3 class="text-xl font-bold text-gray-800 mb-2">{{ event.title }}</h3>
                  <p class="text-gray-600 mb-4">{{ event.description }}</p>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div class="space-y-2">
                      <p class="text-sm text-gray-800">
                        <span class="inline-flex items-center font-semibold">
                          <span class="mr-1.5 text-indigo-500">📍</span>Adresas:
                        </span>
                        {{ event.address }}
                      </p>

                      <p class="text-sm text-gray-800">
                        <span class="inline-flex items-center font-semibold">
                          <span class="mr-1.5 text-indigo-500">🪑</span>Stalo dydis:
                        </span>
                        {{ tableSizeLabels[event.table_size] }}
                      </p>

                      <div v-if="event.first_player_is_organizer && event.players_count === 0"
                           class="py-1 px-3 bg-green-100 text-green-800 rounded-full inline-block text-sm font-medium">
                        🟢 Laisvas - narių 0 - tapk organizatoriumi!
                      </div>
                      <p v-else class="text-sm text-gray-800">
                        <span class="inline-flex items-center font-semibold">
                          <span class="mr-1.5 text-indigo-500">👥</span>Dalyviai:
                        </span>
                        {{ event.players_count || 0 }}
                        <span v-if="event.organizers && event.organizers.length" class="text-green-600 ml-1">
                          (Organizatorius: {{ getOrganizerNames(event) }})
                        </span>
                        <span v-else class="text-green-600 ml-1">
                          (Organizatorius: {{ event.created_by }})
                        </span>
                      </p>

                      <p class="text-sm text-gray-800">
                        <span class="inline-flex items-center font-semibold">
                          <span class="mr-1.5 text-indigo-500">🔒</span>Viešumas:
                        </span>
                        {{ privacyLabels[event.visibility] }}
                      </p>
                    </div>

                    <div class="space-y-2">
                      <p class="text-sm text-gray-800">
                        <span class="inline-flex items-center font-semibold">
                          <span class="mr-1.5 text-indigo-500">🕒</span>Pradžia:
                        </span>
                        {{ formatDateTime(event.start_time) }}
                      </p>

                      <p class="text-sm text-gray-800">
                        <span class="inline-flex items-center font-semibold">
                          <span class="mr-1.5 text-indigo-500">✅</span>Pabaiga:
                        </span>
                        {{ formatDateTime(event.end_time) }}
                      </p>

                      <p v-if="event.perks" class="text-sm text-gray-800">
                        <span class="inline-flex items-center font-semibold">
                          <span class="mr-1.5 text-indigo-500">✨</span>Papildomos galimybės:
                        </span>
                        {{ event.perks }}
                      </p>

                      <div class="mt-4 flex flex-wrap items-center gap-2">
                        <button
                          v-if="event.is_participant"
                          @click="goToEvent(event.id)"
                          class="px-4 py-2 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-lg hover:from-indigo-700 hover:to-blue-700 shadow-sm transition flex items-center gap-1"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          Eiti į renginį
                        </button>
                        <button
                          v-else
                          @click="joinEvent(event.id)"
                          class="px-4 py-2 bg-gradient-to-r from-green-600 to-green-500 text-white rounded-lg hover:from-green-700 hover:to-green-600 shadow-sm transition flex items-center gap-1"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                          </svg>
                          {{ event.first_player_is_organizer && event.players_count === 0 ? 'Tapti organizatoriumi' : 'Prisijungti' }}
                        </button>

                        <!-- Trinimo mygtukas matomas TIK jei esi organizacijos kūrėjas -->
                        <button
                          v-if="userIsCreator"
                          @click="deleteEvent(event.id)"
                          class="px-3 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-600 hover:text-white transition flex items-center gap-1"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                          Ištrinti
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Organizacijos nariai -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden mb-8">
          <div class="h-3 bg-gradient-to-r from-purple-500 to-indigo-600"></div>
          <div class="p-6">
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center">
                <div class="w-10 h-10 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center mr-3">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                </div>
                <h2 class="text-2xl font-bold text-purple-700">Nariai</h2>
                <span class="ml-3 bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
                  {{ members.length }} nariai
                </span>
              </div>

              <!-- User invitation section - only visible to creator -->
              <button
                v-if="userIsCreator"
                @click="showInviteModal = true"
                class="px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 shadow-sm transition flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Kviesti narius
              </button>
            </div>

            <!-- User invitation modal -->
            <div v-if="showInviteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
                <div class="flex justify-between items-center mb-4">
                  <h3 class="text-lg font-semibold text-gray-800">Kviesti narius</h3>
                  <button
                    @click="closeInviteModal"
                    class="text-gray-400 hover:text-gray-600"
                  >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Ieškoti naudotojo
                  </label>
                  <div class="relative">
                    <input
                      v-model="searchQuery"
                      @input="searchUsers"
                      type="text"
                      placeholder="Įveskite vardą arba el. paštą..."
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                    <svg class="absolute right-3 top-2.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>

                <!-- Search results -->
                <div v-if="searchResults.length > 0" class="max-h-60 overflow-y-auto">
                  <h4 class="text-sm font-medium text-gray-700 mb-2">Paieškos rezultatai:</h4>
                  <ul class="space-y-2">
                    <li
                      v-for="user in searchResults"
                      :key="user.id"
                      class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
                    >
                      <div class="flex items-center">
                        <div class="w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-sm font-semibold mr-3">
                          {{ user.username.charAt(0).toUpperCase() }}
                        </div>
                        <div>
                          <p class="font-medium text-gray-800">{{ user.username }}</p>
                          <p class="text-sm text-gray-500">{{ user.email }}</p>
                        </div>
                      </div>
                      <button
                        @click="inviteUser(user.id)"
                        :disabled="invitingUsers.includes(user.id)"
                        class="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:bg-gray-400 transition"
                      >
                        {{ invitingUsers.includes(user.id) ? 'Siunčiama...' : 'Kviesti' }}
                      </button>
                    </li>
                  </ul>
                </div>

                <div v-else-if="searchQuery && searchQuery.length >= 2" class="text-center py-4 text-gray-500">
                  Naudotojų nerasta
                </div>

                <div v-if="!searchQuery || searchQuery.length < 2" class="text-center py-4 text-gray-400 text-sm">
                  Įveskite mažiausiai 2 simbolius paieškai
                </div>
              </div>
            </div>

            <!-- Join requests section - only visible to creator -->
            <div v-if="userIsCreator && joinRequests.length > 0" class="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                <svg class="w-5 h-5 text-yellow-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                Laukiantys prašymai ({{ joinRequests.length }})
              </h3>
              <ul class="space-y-2">
                <li
                  v-for="req in joinRequests"
                  :key="req.id"
                  class="flex justify-between items-center bg-white p-3 rounded-lg border border-yellow-300"
                >
                  <span class="text-gray-800 font-medium">{{ req.user_email }}</span>
                  <button
                    @click="approveRequest(req.id)"
                    class="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 transition"
                  >
                    Patvirtinti
                  </button>
                </li>
              </ul>
            </div>

            <!-- Members list -->
            <div v-if="members.length === 0" class="bg-gray-50 p-10 rounded-lg border border-gray-200 text-center">
              <div class="flex flex-col items-center">
                <svg class="w-12 h-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                <p class="text-gray-500 text-lg font-medium">Šiuo metu nėra narių</p>
                <p class="text-gray-400 mt-1">Pakvieskite žmones prisijungti prie organizacijos</p>
              </div>
            </div>

            <ul v-else class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <li
                v-for="member in members"
                :key="member.id"
                class="p-4 bg-gray-50 border border-gray-200 rounded-lg flex justify-between items-center"
              >
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center text-lg font-semibold mr-3">
                    {{ member.username.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <p class="font-medium text-gray-800">{{ member.username }}</p>

                    <div v-if="userIsCreator">
                      <p class="text-sm text-gray-500">{{ member.first_name }} {{ member.last_name }}</p>
                      <p class="text-sm text-gray-400">{{ member.email }}</p>
                    </div>
                  </div>
                </div>

                <div v-if="canKick(member.id)">
                  <button
                    @click="kickMember(member.id)"
                    class="px-3 py-1.5 bg-red-100 text-red-600 border border-red-200 text-sm rounded-lg hover:bg-red-600 hover:text-white hover:border-red-600 transition flex items-center gap-1"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                    </svg>
                    Išmesti
                  </button>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <OrganizationEditModal
      v-if="organization"
      :visible="showEditModal"
      :organization="organization"
      @close="showEditModal = false"
      @updated="handleUpdated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import OrganizationEditModal from '@/components/OrganizationEditModal.vue'
import axios from '../api/axios'

const route = useRoute()
const router = useRouter()
const token = localStorage.getItem('access')

const organization = ref<any>(null)
const members = ref<any[]>([])
const user = ref<any>(null)
const joinRequests = ref([])

// UI state
const showEditModal = ref(false)
const showInviteModal = ref(false)

// Search functionality
const searchQuery = ref('')
const searchResults = ref([])
const invitingUsers = ref<number[]>([])

// Hardcoded categories matching backend CATEGORY_CHOICES
const categoryOptions = [
  { value: 'classic_strategic', name: 'Klasikiniai & Strateginiai' },
  { value: 'rpg', name: 'RPG (Role-playing games)' },
  { value: 'miniature_games', name: 'Miniatiūrų žaidimai' },
  { value: 'party_social', name: 'Vakarėlių ir socialiniai žaidimai' },
  { value: 'children_games', name: 'Vaikų žaidimai' },
  { value: 'educational', name: 'Edukaciniai žaidimai' }
]

const getCategoryName = (categoryValue: string) => {
  const category = categoryOptions.find(cat => cat.value === categoryValue)
  return category ? category.name : categoryValue
}

const searchUsers = async () => {
  if (searchQuery.value.length < 2) {
    searchResults.value = []
    return
  }

  try {
    const res = await axios.get('/users/search/', {
      params: { q: searchQuery.value },
      headers: { Authorization: `Bearer ${token}` }
    })
    // Filter out users who are already members
    const memberIds = members.value.map(member => member.id)
    searchResults.value = res.data.filter(user => !memberIds.includes(user.id))
  } catch (error) {
    console.error('Error searching users:', error)
    searchResults.value = []
  }
}

const inviteUser = async (userId: number) => {
  if (invitingUsers.value.includes(userId)) return

  invitingUsers.value.push(userId)

  try {
    await axios.post(`/organizations/${organization.value.id}/invite/`, {
      user_id: userId
    }, { headers: { Authorization: `Bearer ${token}` } })

    alert('✅ Kvietimas sėkmingai išsiųstas!')

    // Remove user from search results after successful invitation
    searchResults.value = searchResults.value.filter(user => user.id !== userId)
  } catch (error) {
    console.error('Error inviting user:', error)
    alert('❌ Nepavyko išsiųsti kvietimo. Bandykite dar kartą.')
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

const fetchOrganization = async () => {
  try {
    const orgId = route.params.id
    const response = await axios.get(`/organizations/${orgId}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    organization.value = response.data
  } catch (error) {
    console.error('Error fetching organization:', error)
  }
}

const fetchMembers = async () => {
  try {
    const orgId = route.params.id
    const response = await axios.get(`/organizations/${orgId}/members/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    members.value = response.data
  } catch (error) {
    console.error('Error fetching members:', error)
  }
}

const fetchUser = async () => {
  try {
    const res = await axios.get('/users/me/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = res.data
  } catch (error) {
    console.error('Error fetching user:', error)
  }
}

const fetchJoinRequests = async () => {
  try {
    const res = await axios.get(`/organizations/${route.params.id}/join_requests/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    joinRequests.value = res.data
  } catch (err) {
    console.error('Nepavyko gauti prašymų:', err)
  }
}

const approveRequest = async (requestId) => {
  try {
    await axios.post(`/organizations/${route.params.id}/approve_request/`, { request_id: requestId }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('✅ Prašymas patvirtintas.')
    fetchJoinRequests()
    fetchMembers()
  } catch (err) {
    console.error('Klaida patvirtinant:', err)
    alert('❌ Nepavyko patvirtinti prašymo.')
  }
}

const userIsCreator = computed(() => {
  return organization.value && user.value && organization.value.created_by === user.value.username
})

const joinEvent = async (eventId: number) => {
  try {
    await axios.post(`/events/${eventId}/join/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchOrganization()
  } catch (error) {
    console.error('Error joining event:', error)
    alert('❌ Nepavyko prisijungti prie renginio.')
  }
}

const deleteEvent = async (eventId: number) => {
  if (!confirm('Ar tikrai nori ištrinti šį renginį?')) return

  try {
    await axios.delete(`/events/${eventId}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchOrganization()
    alert('✅ Renginys sėkmingai ištrintas.')
  } catch (error) {
    console.error('Error deleting event:', error)
    alert('❌ Nepavyko ištrinti renginio.')
  }
}

const goToEvent = (eventId: number) => {
  router.push(`/events/${eventId}`)
}

const getOrganizerNames = (event: any) => {
  return event.organizers?.map((org: any) => org.username).join(', ') || ''
}

const formatDateTime = (datetimeStr: string) => {
  return new Date(datetimeStr).toLocaleString('lt-LT', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

const canKick = (memberId: number) => {
  return userIsCreator.value && user.value?.id !== memberId
}

const kickMember = async (memberId: number) => {
  if (!confirm('Ar tikrai norite išmesti šį narį iš organizacijos?')) return

  try {
    const orgId = route.params.id
    await axios.delete(`/organizations/${orgId}/remove-member/${memberId}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchMembers()
    alert('✅ Narys sėkmingai išmestas iš organizacijos.')
  } catch (error) {
    console.error('Error kicking member:', error)
    alert('❌ Nepavyko išmesti nario.')
  }
}

const handleUpdated = async () => {
  await fetchOrganization()
  showEditModal.value = false
}

onMounted(() => {
  fetchOrganization()
  fetchMembers()
  fetchUser()
  fetchJoinRequests()
})

const tableSizeLabels: Record<string, string> = {
  S: 'Mažas (2 žmonės) ~ 80x80cm',
  M: 'Vidutinis (4 žmonės) ~ 120x80cm',
  L: 'Didelis (6–8 žmonės) ~ 180x90cm',
  XL: 'Labai didelis (8–10 žmonių) ~ 200x100cm'
}

const privacyLabels: Record<string, string> = {
  public: '🔓 Vieša – matoma visiems',
  protected: '🔐 Apsaugota – matoma, bet reikia leidimo jungtis',
  private: '🚫 Privati – nematoma, tik pakviestiesiems'
}
</script>
