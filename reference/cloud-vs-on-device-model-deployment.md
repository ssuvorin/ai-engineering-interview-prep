> Source: https://outcomeschool.com/blog/cloud-vs-on-device-model-deployment

# Cloud vs On-device Model Deployment

In this blog, we learn about Cloud vs On-device Model Deployment, the two places where an AI model can run. We cover: what deployment is, training and inference, what Cloud Deployment is, what On-device Deployment is, the one big difference, the round trip problem, where our data goes, how big the model can be, who pays the bill, the shipping problem, what happens when the network is gone, the hybrid approach, some real examples, a table of differences, when to use which one, and a summary.

## What is deployment?

We built an AI model - right now it is just a big file on our computer. Deployment means putting the model somewhere it can run so real people can use it.

Deployment = A model + A place where it runs

Two choices:

- Cloud Deployment: keep the model on a powerful computer far away in a data center, reachable over the internet.
- On-device Deployment (also called Edge Deployment): put the model inside the phone, laptop, car, or camera the person is using. A device can be a phone, laptop, smart watch, car, security camera, smart speaker, or small sensor in a factory.

## Training and inference

An AI model has two phases:

- Training is where the model learns - extremely heavy work, can take thousands of machines running for weeks.
- Inference is where the model answers - we give one question, get one answer. Much lighter.

Analogy: training is a student studying for years (needs a college); inference is the student answering one exam question (needs only a pen).

Training almost always happens in the cloud. So Cloud vs On-device deployment is about inference: where does the model run when a real user asks it something?

## What is Cloud Deployment?

In Cloud Deployment, the model lives on a powerful server in a data center, and the device sends the question over the internet to get the answer. The device itself does almost nothing - collect the question, send it, wait, show the answer.

Example: typing "Explain gravity to a child" in ChatGPT on a phone. The phone packs the sentence into a network request and sends it to a server holding a very large model. The model reads, produces the answer, and sends it back.

```
   Our phone                     Internet                    Cloud server
   [ Question ]  -------------------------------------->  [ Very big model ]
   [  Answer  ]  <--------------------------------------  [     Answer    ]
```

The phone is only a messenger. All real work happens on the server.

Cloud advantages:

- The model can be as big as we want, because the server is powerful.
- We can update the model any time; every user gets the new version instantly.
- The same model serves every user, old or new phone.
- We can watch what happens, collect logs, and fix problems quickly.

Cloud disadvantages:

- The user must have internet.
- Every answer takes a network round trip - delay.
- User data leaves the device and goes to a server owned by someone else.
- We pay for every request forever; the bill never stops.
- If the server goes down, the feature stops working for every user.

## What is On-device Deployment?

In On-device Deployment, the model lives inside the device and the device runs it on its own hardware without contacting any server. No network request, no server, the question never leaves the device.

Example: face unlock on a phone runs an AI model that decides whether this is the owner, in a fraction of a second, even in flight mode.

```
   Our phone
   [ Question ]  ---->  [ Small model ]  ---->  [ Answer ]
              Nothing ever leaves the device
```

Many features are on-device: predictive keyboard, call noise cancellation, "Hey" wake word, offline translation, photo app object search, and self-driving inside a car.

On-device advantages:

- Works without the internet.
- Very fast - no network round trip.
- User data stays on the device - privacy.
- No server bill per request; the user's own hardware does the work.

On-device disadvantages:

- The model must be small (limited memory and power).
- A smaller model is usually less capable than a huge cloud model.
- Running the model drains battery and heats the device.
- Must work on old phones and new phones alike.
- Updating the model means shipping an app update; many users never update.
- Hard to see what went wrong inside the user's device.

## The one big difference

> In Cloud Deployment, the data travels to the model. In On-device Deployment, the model travels to the data.

Everything else comes from this point.

In the cloud, we ship one copy of the model to a data center, and billions of pieces of user data travel to it one request at a time. On the device, we ship a copy of the model to every device once, and then no data travels anywhere.

## The round trip problem

When we send a question to the cloud, data physically travels: phone -> tower -> cables -> data center -> model runs, then the whole journey in reverse for the answer. On a good connection this is around 50-200 ms; worse on weak connections. On-device, that journey does not exist.

For a chat app, 200 ms is fine. For a self-driving car it is not: at 100 km/h, a 200 ms wait means the car has travelled about 5 meters with its eyes closed; a dropped 2-second network means it is blind for more than 50 meters. So safety-critical, instant tasks (noise cancellation, camera effects, keyboard, face unlock) must be on-device.

First rule: if the answer must be instant or the network cannot be trusted, go on-device.

## Where does our data go?

Cloud: user data leaves the device and lands on a machine owned by a company. On-device: data never leaves; nothing to intercept, leak, or store.

This matters for hospitals, banks, keyboards, photo apps, and countries that restrict where data may travel.

Middle option: on-premise deployment - company runs the model on its own servers inside its own building. Data still travels but only inside the company's own network. Gives privacy of on-device with power of the cloud, but the company must buy and maintain expensive hardware.

```
   On-device     [ Data ]                             The data never leaves the device
   On-premise    [ Data ] ---> [ Company's server ]   Leaves device, stays inside company
   Cloud         [ Data ] ---> [ Another company's ]  Leaves device and company
```

Privacy is a distance, not yes/no.

Second rule: if the data is deeply personal or law restricts it from moving, go on-device.

## How big can the model be?

Cloud servers can run models with hundreds of billions of parameters. A phone model is usually a few billion parameters at most, compressed to fit (a few hundred MB to a few GB vs. hundreds of GB cloud model).

Techniques to make a model fit:

- Quantization: store numbers with less precision (e.g., 4 bits instead of 16), shrink to a quarter while keeping most quality.
- Pruning: remove parts that contribute very little.
- Distillation: train a small model to copy the behavior of a big model.

These cannot perform magic; a compressed small model will not match a huge cloud model on hard reasoning, long documents, or deep world knowledge. But the gap is closing every year.

Third rule: if the task needs maximum intelligence, go to the cloud.

## Who pays the bill?

Cloud: cost grows with every user - a running cost forever.

On-device: heavy cost upfront (engineering to shrink the model, make it run on many devices, test everywhere), but once shipped each answer costs nothing. Ten users and ten million users cost the same.

The on-device cost line starts high and stays flat; the cloud line starts near zero and keeps climbing. Before the crossing point cloud is cheaper; after it, cloud becomes far more expensive.

Catch: the cost moves to the user in battery life, storage space, and a warm phone.

Fourth rule: with a huge number of users doing a simple, repeated task, on-device saves a lot of money.

## The shipping problem

Cloud: fix the model on Monday morning, by Monday afternoon every user has it. Devs who experiment a lot prefer the cloud.

On-device: model must be downloaded (2 GB app, or separate download after launch - users abandon during the wait), and updates crawl out slowly. A fix reaches roughly: 0% on Monday, 30% by Day 3, 70% by Week 2, 85% by Month 2, ~90% later and it stops there. Some users never update. Device hardware varies (three-year-old budget phone vs. flagship).

Fifth rule: if we need to change the model often, or cannot afford a large download, the cloud is safer.

## What happens when the network is gone?

A traveler in a new country with no SIM and broken airport WiFi points the camera at a sign in an unknown language. Cloud: spinner then error. On-device: translation shown right there.

The cloud path has a broken link in a network segment sufficing to stop the whole feature. On-device has no link that can break. Same applies in villages, basement parking lots, metro tunnels, and airplanes.

Sixth rule: if the feature must keep working without the internet, it has to be on-device.

## The hybrid approach

In the hybrid approach, a small model runs on the device and handles easy work, and the big cloud model is called only when the task is genuinely hard.

```
        [ User's question ]
                v
     [ Small model on the device ]
        Can I handle this?
        +-------+-------+
       Yes              No
        |               |
        v               v
   [ Answer on     [ Send to the big
     the device ]    cloud model ]
                          v
                     [ Answer ]
```

Most questions get answered on-device quickly and privately; only the difficult ones go to the cloud.

## Some real examples

Chat apps, image generation, and general assistants are in the cloud. Face unlock, predictive keyboard, noise cancellation, wake words, offline translation, photo searches, and self-driving systems run on-device. Hospitals, banks, and government departments use on-premise.

## The difference (table)

| Aspect | Cloud Deployment | On-device Deployment |
| --- | --- | --- |
| Where the model runs | Data center server | Inside the device |
| Internet required | Yes | No |
| Latency | Round-trip delay | Near-zero |
| Data privacy | Data leaves the device | Data never leaves |
| Model size | Can be very large | Must be small |
| Cost model | Per-request, grows forever | One-time engineering cost, then flat (cost moves to user) |
| Updates | Instant for all | Slow app updates, some never |
| Failure | Single point, no fallback | Works offline |

## When to use which one?

- Instant response, offline, or private data -> on-device.
- Maximum intelligence, frequent model updates, no download concerns -> cloud.
- Both -> hybrid.

## Summary

In Cloud Deployment, the data travels to the model; in On-device Deployment, the model travels to the data. The choice is a trade-off between intelligence (cloud) and speed/privacy/offline (device), with hybrid as the practical middle ground.
