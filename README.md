# 🌐 Turkcell NIQS - Network & System Health Service

![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

> **Cloud-Native 2-Tier Microservice Architecture on Kubernetes / OpenShift**
>
> Lokal Docker ortamından, kurumsal seviye (Enterprise) Kubernetes kümesine geçiş ve orkestrasyon projesi.

---

## 📋 Proje Hakkında

Bu proje, ağ cihazlarının (Router, Switch vb.) metriklerini (latency, packet loss) toplayan, veritabanına kaydeden ve dış dünyaya REST API üzerinden sunan **2 katmanlı (2-Tier) Mikroservis Mimarisi** projesidir.

Projenin asıl odak noktası uygulamanın kendisi değil, uygulamanın çalıştırıldığı **altyapıdır**. Kodlanmış bir servisin Kubernetes üzerinde nasıl sıfır kesintiyle çalıştırıldığı, verilerin nasıl kalıcı hale getirildiği ve şifrelerin nasıl izole edildiği kanıtlanmıştır.

**Öne Çıkan Kubernetes Yetenekleri:**
* 💾 **Kalıcı Depolama (Persistence):** `PersistentVolumeClaim (PVC)` ile veritabanı silinse bile sıfır veri kaybı.
* 🛡️ **Güvenlik & İzolasyon:** Şifrelerin ve ortam değişkenlerinin `Secret` ve `ConfigMap` ile yönetilmesi.
* ♻️ **Kendi Kendini İyileştirme (Self-Healing):** Çöken Pod'ların anında tespit edilip yeniden başlatılması.
* 🏥 **Sağlık Kontrolleri:** `Liveness` ve `Readiness` probları ile trafik yönlendirmesinin güvenli yönetimi.

---

## 🏛️ Mimari Şema

```text
[ Tarayıcı / İstemci ]
        │
        ▼ (Port: 8000)
┌─────────────────────────────────────────────────────────┐
│                   niqs-api-service                      │
│                  (Kubernetes Service)                   │
└───────────────────────────┬─────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐
│   niqs-api-pod 1      │       │   niqs-api-pod 2      │
│  (Python FastAPI)     │       │  (Python FastAPI)     │
└───────────┬───────────┘       └───────────┬───────────┘
            │                               │
            └───────────────┬───────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   postgres-service                      │
│                  (Internal Port: 5432)                  │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     postgres-pod                        │
│                 (PostgreSQL Database)                   │
└───────────────────────────┬─────────────────────────────┘
                            │ (Mount: /var/lib/postgresql/data)
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   postgres-pvc                          │
│            (PersistentVolumeClaim - 1Gi)                │
└─────────────────────────────────────────────────────────┘
